import { createApp } from 'vue'
import router from './router'
import './style.css'
import App from './App.vue'
import store from './store'
import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'

createApp(App)
.use(router)
.use(store)
.use(bootstrap)
.mount('#app')
