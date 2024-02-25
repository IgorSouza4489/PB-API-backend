<template>
  <div id="container">
    <div id="barraZ">
      <div class="form-container">
        <form @submit.prevent="login">
          <div class="form-group">
            <h1>Login</h1>
            <br />

            <input-form
              label="Email"
              type="text"
              v-model="email"
              placeholder="Digite um email"
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
              value="Entrar"
            />
            <div v-if="showIframe" class="overlay">
              <iframe
                id="load"
                src="https://lottie.host/embed/4a40d72c-2547-4f2a-909c-2044e6b7717e/xIffzuE3W0.json"
              ></iframe>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
import InputForm from "./Form/InputForm.vue";
import api from "./api";
import { useToast } from "vue-toastification";

const toast = useToast();
export default {
  name: "LoginPage",
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
      erro: false,
      showIframe: false,
    };
  },
  created() {},
  methods: {
    async login() {
      this.showIframe = true;
      
      try {
        const response = await api.post("/login", {
          email: this.email,
          senha: this.senha,
        });
        console.log(response.data);
        setTimeout(() => {
        this.showIframe = false;
        toast.success("Seja bem vindo!");
        this.$router.push({
          path: "/HomePage",
          //query: {id: tipo}
        });
      }, 1500);
        
      } catch (error) {
        this.erro = true;
        toast.error("Ocorreu algum erro ao tentar entrar, verifique suas credenciais");
        this.showIframe = false;
      }
      
    },
  },
};
</script>

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

