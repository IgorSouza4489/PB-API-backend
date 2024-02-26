import LoginPage from "../components/LoginPage.vue";
import '../assets/global.css'

describe('LoginPage Component', () => {
  beforeEach(() => {
    cy.mount(LoginPage);
  });

  it('Mostar Login', () => {
    cy.get('.form-container').should('exist');
    cy.get('form').should('exist');
    cy.get('input[type="text"]').should('exist');
    cy.get('input[type="password"]').should('exist');
    cy.get('input[type="submit"]').should('exist');
  });

  it('Testar Login Certo', () => {
    cy.get('input[type="text"]').type('lag@gmail.com');
    cy.get('input[type="password"]').type('123');
    cy.get('form').submit();

    cy.url().should('include', '/HomePage');
    
    cy.get('.toast-success').should('exist');
  });

  it('Testar Login Erro', () => {
    cy.get('input[type="text"]').type('invalid@example.com');
    cy.get('input[type="password"]').type('invalidpassword');
    cy.get('form').submit();

    cy.get('.toast-error').should('exist');
  });
});
