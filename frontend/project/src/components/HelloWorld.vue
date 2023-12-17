<template>
  <div id="container">
    <div id="barraZ">
      <div class="form-container">
        <form @submit.prevent="register">
            <div class="form-group">
              <h1>Registrar </h1><br>

              <input-form label="Nome" type="text"  v-model="nome" placeholder="Digite um nome" />
            </div>
            <div class="form-group">
              <input-form label="Nome" type="text"  v-model="nome" placeholder="Digite seu email" />
            </div>
            <div class="form-group">
              <input-form label="Data de Nascimento" type="date" v-model="dataInicio" placeholder="Selecione sua data de nascimento" />
            </div>
            <div class="form-group">
              <input-form label="Senha" type="password" v-model="senha" placeholder="Digite uma senha" />
            </div>
            <div class="form-group">
            <input type="submit" id="btn" value="Registrar"  @click.prevent="showIframe = true"> 
            <div v-if="showIframe" class="overlay">
              <iframe id="load" src="https://lottie.host/embed/4a40d72c-2547-4f2a-909c-2044e6b7717e/xIffzuE3W0.json"></iframe>
            </div>   
            </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import InputForm from './Form/InputForm.vue';

//import api from './api';

export default {
  name: 'HelloWorld',
  components:{
    InputForm
  },
  props: {
    msg: String
  },
  data(){
    return{
      email: '',
      senha: '',
      nome: '',
      nascimento: '',
      erro: false,
      showIframe: false,
    }
  },
  created(){

  },
  methods: {
    async register(){


      this.showIframe = false;

    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
body.overlay {
  overflow: hidden; /* Impede a rolagem da página quando o fundo estiver opaco */
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}
</style>
