import { createRouter, createWebHashHistory } from 'vue-router'
import LoginForm from '../components/LoginForm.vue'
import RegisterForm from '../components/RegisterForm.vue'
import FileList from '../components/FileList.vue'
import store from '../store'


const routes = [
  {path: '/login', component: LoginForm},
  {path: '/register', component: RegisterForm},
  {
    path: '/',
    name: 'filelist',
    component: FileList,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth) && !store.getters.isAuthenticated) {
    next("/login");
  } else {
    next();
  }
});

export default router
