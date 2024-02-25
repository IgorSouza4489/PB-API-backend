import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '@/components/HelloWorld.vue'
import LoginPage from '@/components/LoginPage.vue'
import HomePage from '@/components/HomePage.vue'


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
      component: HomePage
    },   
]

const router = createRouter({
    history: createWebHistory(),
    routes
  })




export default router