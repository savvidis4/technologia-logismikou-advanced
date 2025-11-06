# app/business/signin_service.py

"""
=============================================================
 Business Logic Layer - Sign In 
=============================================================
Η κλάση SignInService είναι υπεύθυνη για τη λογική σύνδεσης χρηστών.
Δεν περιλαμβάνει καμία UI ή controller λογική.

Δέχεται db_session μέσω dependency injection και ελέγχει αν το email
και ο κωδικός ταιριάζουν με αυτά της βάσης.
"""

from app.models import User, Account


class SignInService:

    def __init__(self, db_session):

        """
        Constructor με dependency injection.

        :param db_session: Ενεργό SQLAlchemy session
        """

        self.db = db_session

    # =========================================================
    # Κύρια μέθοδος για έλεγχο credentials
    # =========================================================
    def verify_credentials(self, current_user_id, email, password):
        """
        Ελέγχει αν τα credentials είναι σωστά.

        1. Αναζητά τον χρήστη στη βάση μέσω ORM.
        2. Συγκρίνει τον αποθηκευμένο κωδικό με τον δοθέντα.
        3. Επιστρέφει ένα business-friendly αποτέλεσμα (dict).

        :email: Email του χρήστη (string)
        :password: Κωδικός πρόσβασης (string)
        :return: dict με αποτέλεσμα (success, message, id, username)
        """

        # Αναζήτηση χρήστη
        user = User.query.get(current_user_id)
        account = Account.query.filter_by(user_id=current_user_id).first()

        # Αν δεν βρεθεί ο χρήστης
        if not user or not account:
            return {
                "success": False,
                "message": "User not found"
            }

         # Έλεγχος email
        if user.email != email:
            return {
                "success": False,
                "message": "Lathos Email."
            }


        # Έλεγχος password
        if user.password != password:
            return {
                "success": False,
                "message": "Lathos Kwdikos."
            }

        # Αν όλα είναι εντάξει → δημιουργούμε “λογικό” αποτέλεσμα
        return {
            "success": True,
            "message": "Login successful.",
            "user": {
                "id": user.id,
                "username": user.username,
            }
        }