<template>
  <div id="container">
    <div id="barraZ">
      <div class="form-container">
        <form @submit.prevent="register">
          <div class="form-group">
            <h1>Registrar</h1>
            <br />

            <input-form
              label="Nome"
              type="text"
              v-model="nome"
              placeholder="Digite um nome"
            />
          </div>
          <div class="form-group">
            <input-form
              label="Email"
              type="text"
              v-model="email"
              placeholder="Digite seu email"
            />
          </div>
          <div class="form-group">
            <input-form
              label="Data de Nascimento"
              type="date"
              v-model="data_nascimento"
              placeholder="Selecione sua data de nascimento"
            />
          </div>
          <div class="form-group">
            <input-form
              label="Senha"
              type="password"
              v-model="senha"
              placeholder="Digite uma senha"
            />
          </div>
          <div class="form-group">
            <input
              type="submit"
              id="btn"
              value="Registrar"
               :disabled="!registraHabilitado"
            />
            <div v-if="showIframe" class="overlay">
              <iframe
                id="load"
                src="https://lottie.host/embed/4a40d72c-2547-4f2a-909c-2044e6b7717e/xIffzuE3W0.json"
              ></iframe>
            </div>
            <div id = "lowKey">
                <a @click="navegarParaLogin" id="">Já tem uma conta? Clique aqui!</a>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import InputForm from "./Form/InputForm.vue";
import { useToast } from "vue-toastification";
const toast = useToast();
import api from "./api";

export default {
  name: "HelloWorld",
  components: {
    InputForm,
  },
  props: {
    msg: String,
  },
  data() {
    return {
      email: "",
      senha: "",
      nome: "",
      data_nascimento: "",
      erro: false,
      showIframe: false,
    };
  },
  created() {},
  methods: {
    async register() {
      this.showIframe = true
      try {
        const response = await api.post("/usuarios", {
          nome: this.nome,
          email: this.email,
          data_nascimento:'01/01/2022' /*new Date(this.data_nascimento)*/,
          senha: this.senha,
        });

        console.log(response.data);
        toast.success("Conta criada com sucesso!");
        this.$router.push({
          path: "/LoginPage",
          //query: {id: tipo}
        });
      } catch (error) {
        this.erro = true;
        toast.success("Erro ao criar conta");
        console.error(error);
      }
        setTimeout(() => {
        this.showIframe = false;
      }, 1500);

    },
    navegarParaLogin(){
      this.$router.push({path: '/LoginPage'})
    }
  },
   computed: {
    registraHabilitado() {
      return (
        this.nome !== "" &&
        this.email !== "" &&
        this.dataInicio !== "" &&
        this.senha !== ""
      );
    },
  },
};
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

