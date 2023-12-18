<template>
  <div style="text-align:center !important; ">
    <div id="sidebar">
      <div id="sidebar-header">
        <h3>coRecs</h3>
      </div>
      <div id="sidebar-menu">
        <router-link to="/feed">Feed</router-link>
        <router-link to="/minha-conta">Minha Conta</router-link>
        <button @click="sair">Sair</button>
      </div>
    </div>

    <div class="container">
      <div id="headerTitle" class="mb-3">
        <input type="text" v-model="termoPesquisa" class="form-control" placeholder="Pesquisar">
        
      </div>
      <div class="container" style="padding-bottom:50px"> 
        <criar-postagem ></criar-postagem>
      </div>


      <div v-if="postagens.length === 0">
        <p>Nenhuma postagem disponível.</p>
      </div>

      <div class="post" v-for="postagem in postagens" :key="postagem.id">
        <div class="post-header">
          <div>
            <h5>{{ postagem.nome_autor }}</h5>
          </div>
        </div>
        <hr>
        <div class="post-content">
          <p>{{ postagem.texto }}</p>
          <p>{{ formatarData(postagem.datahora_postagem) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "./api";
import CriarPostagem from "./CriarPostagem.vue";

export default {
  name: "HomePage",
  components: {
    CriarPostagem,
  },
  data() {
    return {
      postagens: [],
      termoPesquisa: "",
    };
  },
  mounted() {
    this.getPostagens();
  },
  methods: {
    async getPostagens() {
      try {
        const response = await api.get("/postagens");
        this.postagens = response.data.postagens;
      } catch (error) {
        console.log(error);
      }
    },
    formatarData(data) {
      const dataObj = new Date(data);
      return `${dataObj.toLocaleDateString()} ${dataObj.toLocaleTimeString()}`;
    },
    sair() {
      console.log("Usuário saiu");
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.post {
  border: 1px solid #ccc;
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 8px;
}

.post-header {
  display: flex;
  align-items: center;
}

.post-content {
  margin-top: 10px;
}

#headerTitle {
  margin: 20px;
  display: flex;
  align-items: center;
}

#headerTitle input {
  margin-left: auto;
  padding: 5px;
}

#sidebar {
  background-color: #333;
  color: white;
  width: 200px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
}

#sidebar-header {
  padding: 20px;
  text-align: center;
  background-color: #ff5e00;
}

#sidebar-menu {
  display: flex;
  flex-direction: column;
  padding: 10px;
}

#sidebar-menu a,
#sidebar-menu button {
  color: white;
  text-decoration: none;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #444;
  border: none;
  cursor: pointer;
}

#sidebar-menu a:hover,
#sidebar-menu button:hover {
  background-color: #555;
}

</style>
