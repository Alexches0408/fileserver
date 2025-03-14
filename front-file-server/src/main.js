import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from "./store"
import axios from 'axios'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

axios.defaults.baseURL = "http://127.0.0.1:8000"

createApp(App).use(router).use(store).mount('#app')

