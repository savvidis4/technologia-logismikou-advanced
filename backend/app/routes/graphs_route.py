# app.py (ή routes.py)
from flask import Blueprint, Blueprint, jsonify, request
from collections import Counter, defaultdict
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Account, Transactions
from app.business.transactions_service import TransactionsService
from app.extensions import db

graphs_bp = Blueprint('graphs', __name__)

@graphs_bp.route('/graphs', methods=['GET', 'POST'])
@jwt_required()
def graphs():
    # 1. Παίρνουμε τα transactions (όπως έκανες στο desktop)
    # Προσοχή: Εδώ υποθέτω ότι το transactions είναι list of tuples/dicts
    
    current_user_id = int(get_jwt_identity())
    
    # 1. Παίρνουμε τα δεδομένα (ΛΙΣΤΑ, όχι json ακόμα)
    transactions_service = TransactionsService(db.session, current_user_id)
    transactions = transactions_service.transactions_list

    # ... (αρχή συνάρτησης graphs) ...

    # Αρχικοποίηση λιστών
    months = []
    types = []
    ins_outs = defaultdict(lambda: {"in": 0, "out": 0})

    print(f"DEBUG: Processing {len(transactions)} transactions...") # Debug print

    for row in transactions:
        try:
            # ΒΑΣΕΙ ΤΟΥ LOG ΠΟΥ ΕΣΤΕΙΛΕΣ:
            # row[3] -> amount
            # row[4] -> currency
            # row[5] -> date
            # row[6] -> type

            # 1. Έλεγχος Νομίσματος (Index 4)
            currency = row[4]

            # Στη βάση γράφει 'EUR', όχι 'Euro (€)'
            if currency == 'EUR': 
                
                # 2. Ημερομηνία (Index 5)
                dt_obj = row[5]
                if not isinstance(dt_obj, str):
                    dt_str = str(dt_obj)
                else:
                    dt_str = dt_obj
                
                # Κόβουμε τα πρώτα 10 γράμματα (YYYY-MM-DD)
                dt = datetime.strptime(dt_str[:10], "%Y-%m-%d")
                month_str = dt.strftime("%b %Y")
                sort_key = dt.strftime("%Y-%m")

                months.append(month_str)
                
                # 3. Τύπος (Index 6)
                t_type = row[6] 
                types.append(t_type)

                # 4. Ποσό (Index 3)
                # Καθαρίζουμε το string (π.χ. "+2340.6" ή "-1000")
                amount_str = str(row[3]).replace('+', '')
                # Χρησιμοποιούμε abs() για να φαίνονται θετικές οι μπάρες στο γράφημα
                amount = abs(float(amount_str)) 

                # 5. Ομαδοποίηση
                full_key = (sort_key, month_str)
                
                # Προσοχή: Στη βάση σου το CREDIT έχει αρνητικό πρόσημο (-1000)
                # και το DEBIT θετικό (+2340). 
                # Το Transaction Type Distribution θέλει απλά να μετρήσει πλήθος.
                
                if str(t_type).upper() == "CREDIT":
                    ins_outs[full_key]["in"] += amount
                elif str(t_type).upper() == "DEBIT":
                    ins_outs[full_key]["out"] += amount
        
        except Exception as e:
            print(f"Skipping row due to error: {row} -> {e}")
            continue

    # ... (συνέχεια με month_counts και return jsonify) ...


    # ... (ο κώδικας μετά το loop για την ετοιμασία JSON παραμένει ίδιος) ...

    # 3. Ετοιμασία δεδομένων για Chart.js
    
    # Γράφημα 1: Συναλλαγές ανά μήνα
    month_counts = Counter(months)
    # Ταξινόμηση με βάση το ημερολογιακό έτος/μήνα είναι καλύτερη στο web
    
    # Γράφημα 2: Κατανομή Τύπου (Pie Chart)
    type_counts = Counter(types)
    pie_data = {
        "labels": list(type_counts.keys()),
        "data": list(type_counts.values())
    }

    # Γράφημα 3: In/Out (Bar Chart)
    # Ταξινομούμε τα κλειδιά βάσει του sort_key (YYYY-MM)
    sorted_keys = sorted(ins_outs.keys(), key=lambda x: x[0])
    
    final_months_labels = [k[1] for k in sorted_keys] # Π.χ. ["Jan 2024", "Feb 2024"]
    in_values = [ins_outs[k]["in"] for k in sorted_keys]
    out_values = [ins_outs[k]["out"] for k in sorted_keys]

    bar_data = {
        "labels": final_months_labels,
        "datasets": [
            {"label": "In (CREDIT)", "data": in_values, "backgroundColor": "#2e7d32"},
            {"label": "Out (DEBIT)", "data": out_values, "backgroundColor": "#c70000"}
        ]
    }
    
    # Γράφημα 1 (Bar Count) - Φτιαγμένο σωστά
    count_data = {
        "labels": list(month_counts.keys()),
        "data": list(month_counts.values())
    }

    return jsonify({
        "pie_chart": pie_data,
        "bar_in_out": bar_data,
        "count_chart": count_data
    }), 200