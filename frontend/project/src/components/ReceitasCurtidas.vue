<template>
  <div>
    <ul class="postagens-list">
      <li v-for="(postagem, index) in postagensMaisCurtidas" :key="index" class="postagem-item">
        <div class="postagem-info">
          <p class="postagem-titulo">{{ postagem.titulo }}</p>
        <img style="border-radius: 50%; width:30%" :src="postagem.url_img" width="100%" alt="">

          <p class="postagem-curtidas">{{ postagem.num_curtidas }} curtidas</p>
          <p class="postagem-autor">Autor: {{ postagem.nome_autor }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import api from "./api";

export default {
  name: "ReceitasCurtidas",
  data() {
    return {
      postagensMaisCurtidas: [],
    };
  },
  async created() {
    this.carregarReceitasCurtidas()
  },
  methods: {
    async carregarReceitasCurtidas() {
    try {
      const response = await api.get('postagens-mais-curtidas');
      this.postagensMaisCurtidas = response.data.postagens_mais_curtidas;
    } catch (error) {
      console.error(error);
    }
    }
  }
};
</script>

<style scoped>
.postagens-list {
  list-style-type: none;
  padding: 0;
}

.postagem-item {
  border-bottom: 1px solid #ddd;
  margin-bottom: 10px;
  padding-bottom: 10px;
}

.postagem-info {
  background-color: transparent; /* Cor base para as informações da postagem */
  padding: 10px;
  border-radius: 5px;
}

.postagem-titulo {
  font-weight: bold;
  color: #333333; /* Cor branca para o título */
}

.postagem-curtidas {
  color: #333333; /* Cor branca para o número de curtidas */
}

.postagem-autor {
  font-style: italic;
  color: #333333; /* Cor cinza claro para o nome do autor */
}
</style>
