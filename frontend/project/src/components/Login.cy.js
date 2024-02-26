import LoginPage from "./LoginPage.vue";
import '../assets/global.css'

it('display login', () => {
    cy.mount(LoginPage)
})
