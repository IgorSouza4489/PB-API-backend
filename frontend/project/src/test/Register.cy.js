import HelloWorld from "../components/HelloWorld.vue";
import '../assets/global.css';

it('mostrar registro', () => {
  cy.mount(HelloWorld);

  cy.get('.component input[placeholder="Digite um nome"]').type('kok2o');
  cy.get('.component input[placeholder="Digite seu email"]').type('joh22n2@gmail.com');
  cy.get('.component input[placeholder="Selecione sua data de nascimento"]').type('2001-01-01');
  cy.get('.component input[placeholder="Digite uma senha"]').type('123');

  cy.get('form').submit();

  cy.url().should('include', '/LoginPage');
});
