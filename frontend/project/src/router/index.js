import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '@/components/HelloWorld.vue'
import LoginPage from '@/components/LoginPage.vue'

const routes = [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },   

    {
      path: '/LoginPage',
      name: 'LoginPage',
      component: LoginPage
    },   
]

const router = createRouter({
    history: createWebHistory(),
    routes
  })




export default router