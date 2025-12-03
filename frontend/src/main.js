import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// ΚΑΝΩ IMPORT ΤΗΝ CSS ΓΙΑ ΚΑΘΕ ΑΡΧΕΙΟ ΞΕΧΩΡΙΣΤΑ
import './assets/home_style.css'
import './assets/login_style.css'

const app = createApp(App)

app.use(router)

app.mount('#app')
