<template>
  <div class="criar-postagem">
    <form id="test" @submit.prevent="criarPostagem">
      <div class="form-group">
        <input placeholder="Título" type="text" v-model="titulo" class="form-control" required>
      </div>
      <div class="form-group">
        <textarea placeholder="Qual a receita de hoje?" v-model="texto" class="form-control" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Criar Postagem</button>
    </form>
  </div>
</template>

<script>
import api from "./api";

export default {
  name: "CriarPostagem",
  data() {
    return {
        titulo: "",
        texto: "",
    };
  },
  methods: {
    async criarPostagem() {
      try {
        const response = await api.post("/postagens", {
          titulo: this.titulo,
          texto: this.texto,
          nome_autor: 'autor'
        });

        console.log(response.data);
        
      } catch (error) {
        this.erro = true;
        console.error(error);
      }


    },
  },
};
</script>

<style scoped>
  form {

    max-width: 100% !important;
    box-shadow: none;

  }
</style>
