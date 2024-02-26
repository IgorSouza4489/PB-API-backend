import HelloWorld from "../components/HelloWorld.vue";
import '../assets/global.css';

it('mostrar registro', () => {
  cy.mount(HelloWorld);

  cy.get('.component input[placeholder="Digite um nome"]').type('John Doe');
  cy.get('.component input[placeholder="Digite seu email"]').type('john@example.com');
  cy.get('.component input[placeholder="Selecione sua data de nascimento"]').type('2000-01-01');
  cy.get('.component input[placeholder="Digite uma senha"]').type('securePassword');

  cy.get('form').submit();

  //cy.wait(1500);

  cy.url().should('include', '/LoginPage');
  cy.get('.toast-success').should('exist');
});
