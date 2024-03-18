import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '@/components/HelloWorld.vue'
import LoginPage from '@/components/LoginPage.vue'
import HomePage from '@/components/HomePage.vue'
import { jwtDecode } from "jwt-decode";
import { useToast } from "vue-toastification";
const toast = useToast();

function checarLogin() {
  const token = localStorage.getItem('access_token')
  if (token) {
    const decodedToken = jwtDecode(token)
    if (decodedToken.exp < Date.now() / 1000) {
      toast.error("Sua sessão expirou, entre em sua conta de usuário para acessar as funcionalidades")
      return false
    } else {
      return true
    }
  } else {
    toast.error("Sua sessão expirou, entre em sua conta de usuário para acessar as funcionalidades")
    return false
  }
}

const routes = [
  

    {
      path: '/LoginPage',
      name: 'LoginPage',
      component: LoginPage
    },  
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },   
    {
      path: '/HomePage',
      name: 'HomePage',
      component: HomePage,
      meta: {
        requiresAuth: true
      },
    },   
]

const router = createRouter({
    history: createWebHistory(),
    routes
  })

  router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
      if (checarLogin()) {
        next()
      } else {
        next('/LoginPage')
      }
    } else {
      next()
    }
  });


export default router