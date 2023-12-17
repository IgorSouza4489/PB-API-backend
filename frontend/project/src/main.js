import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/global.css'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import 'bootstrap/dist/css/bootstrap.min.css'
import 'jquery/src/jquery.js'
import 'bootstrap/dist/js/bootstrap.min.js'
import 'bootstrap/dist/css/bootstrap.css';


const app = createApp(App)
app.use(Toast)
app.use(router)
app.mount('#app')
