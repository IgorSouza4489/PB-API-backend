<template>
  <div class="criar-postagem">
    <form @submit.prevent="criarPostagem" class="form">
      <div class="form-group">
        <input
          v-model="titulo"
          type="text"
          placeholder="Título"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <textarea
          v-model="texto"
          @input="contarCaracteres"
          :placeholder="`Qual a receita de hoje? (Máximo ${limiteCaracteres} caracteres)`"
          class="form-control"
          required
        ></textarea>
        <p>{{ caracteresRestantes }} caracteres restantes</p>
      </div>
      <button
        type="submit"
        class="btn btn-primary"
        :disabled="caracteresRestantes < 0" >
        Criar Postagem
      </button>
    </form>
  </div>
</template>
<script>
import api from "./api";
import { jwtDecode } from "jwt-decode";
import { useToast } from "vue-toastification";
const toast = useToast();

export default {
  name: "CriarPostagem",
  data() {
    return {
      titulo: "",
      texto: "",
      usuario_id: "",
      nome_autor: "",
      limiteCaracteres: 280, 
      caracteresRestantes: 280, 
    };
  },
  async created() {
    const token = localStorage.getItem("access_token");
    if (!token) {
      console.log('Sem token');
    } else {
      const decToken = jwtDecode(token);
      this.usuario_id = decToken.sub;
      const user = JSON.parse(localStorage.getItem('user'));
      this.nome_autor = user.nome;
      console.log(this.nome_autor)
    }
  },
  methods: {
    async criarPostagem() {
      try {
        const response = await api.post("/postagens", {
          titulo: this.titulo,
          url_img: 'ss',
          texto: this.texto,
          nome_autor: this.nome_autor,
          usuario_id: this.usuario_id
        });
        this.$emit('novaPostagemCriada', {
          id: response.data.id, 
          titulo: this.titulo,
          texto: this.texto,
          nome_autor: this.nome_autor,
          usuario_id: this.usuario_id,
          datahora_postagem: new Date().toISOString(), 
          numCurtidas: 0, 
          comentarios: []
        });
        toast.success("Postagem feita com sucesso!");
        this.$router.push({
          path: "/HomePage",
        });
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    },
    contarCaracteres() {
      this.caracteresRestantes = this.limiteCaracteres - this.texto.length;
    },
  },
};
</script>

<style scoped>
.criar-postagem {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.form {
  max-width: 100%;
  width: 100%;
}

.form-group {
  margin-bottom: 1rem;
}

.btn-primary {
  width: 100%;
  background-color: #f85f00;
  border: #f85f00;
}

.btn-primary:hover {
  background-color: #fc9c43 !important;
}

.btn-primary:active {
  background-color: #fc9c43 !important;
}

.btn-primary:focus {
  background-color: #fc9c43 !important;
}
.btn-primary:disabled {
  background-color: #fc9c43 !important;
}
</style>
