<template>
  <div style="text-align:center !important; ">
     <div id="sidebar-header">
    <nav class="navbar navbar-expand-lg navbar-light ">
  <a class="navbar-brand" href="#">receitas.py</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavDropdown">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link" href="#"><router-link to="/feed">Feed</router-link><span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#"><router-link to="/minha-conta">Minha Conta</router-link></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#"><router-link to="/">Minhas Curtidas</router-link></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#"><router-link to="/">Minhas Receitas</router-link></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" @click="sair" href="#">Sair</a>
      </li>
    </ul>
  </div>
</nav>
</div>

    <div id="sidebar">
      <div id="sidebar-profile">
        <a href=""><img src="" alt=""></a>
        <h5>{{usuario.nome}}</h5>
        <h5>{{usuario.email}}</h5>
        <hr>
      </div>
      <div id="sidebar-menu">
        <router-link to="/feed">Feed</router-link>
        <router-link to="/minha-conta">Minha Conta</router-link>
        <router-link to="/">Minhas Curtidas</router-link>
        <router-link to="/">Minhas Receitas</router-link>

        <button @click="sair">Sair</button>
      </div>
      
    </div>


      <div id="sidebar2">
      
      <div id="sidebar-profile2">
        <a href=""><img src="" alt=""></a>
        <h5>Receitas mais curtidas</h5>
        <hr>
      </div>
      <div id="sidebar-menu2">
        

        
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
import { jwtDecode } from "jwt-decode";
import { useToast } from "vue-toastification";
const toast = useToast();

export default {
  name: "HomePage",
  components: {
    CriarPostagem,
  },
  data() {
    return {
      user: '',
      id: '',
      postagens: [],
      termoPesquisa: "",
      usuario: {
        nome: "Igor Santos",
        idade: 25,
        email: "igor@gmail.com"
    },
    };
  },
  async created() {
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error("Não tem token");
    } else {
        const decToken = jwtDecode(token);
        const userId = decToken.sub; // Obtém o ID do usuário do token JWT

        // Agora você pode chamar a função getUserData() com o ID do usuário
        await this.getUserData(userId);
    }
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
    async getUserData(userId) {
    try {
        const response = await api.get(`obter_usuarios?id=${userId}`);
        this.usuario = response.data;
        localStorage.setItem("user", JSON.stringify(this.usuario));
    } catch (error) {
        console.error(error);
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
  max-width: min(600px, 100vw);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.post {
  border: 1px solid #ccc;
  background-color: #e2e2e2;
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
  background-color: #ffffff;
  color: white;
  width: 300px;
  height: 100vh;
  position: absolute;
  top: 5;
  left: 0;
  flex-direction: column;

  
}

#sidebar-header nav{
  padding: 20px;
  text-align: center;
  background-color: #ff5e00;
  color: white;
}
#sidebar-header .dropdown{
  float: right;
  
}
#sidebar-header  h3{
  text-align: left !important;
  padding-left: 50px;
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
  margin: 10px;
  background-color: #ff7b00;
  border-radius: 15px;
  
  border: none;
  cursor: pointer;
}

#sidebar-menu a:hover,
#sidebar-menu button:hover {
  background-color: #fc9c43;
}

#sidebar-profile {
  
}
#sidebar-profile h5{
  color: #000000;
  
}

a{
  color: white !important;
}

@media only screen and (min-width: 992px) {
  #navbarNavDropdown .navbar-nav {
  display: none;
  }

}

@media only screen and (max-width: 992px) {

  #sidebar{
    display: none;
  }
  #sidebar2{
    display: none;
  }
}

















#sidebar2 {
  background-color: #ffffff;
  color: white;
  width: 300px;
  height: 100vh;
  position: absolute;
  top: 5;
  right: 0;
  flex-direction: column;

  
}



#sidebar-menu2 {
  display: flex;
  flex-direction: column;
  padding: 10px;
}

#sidebar-menu2 a,
#sidebar-menu2 button {
  color: white;
  text-decoration: none;
  padding: 10px;
  margin: 10px;
  background-color: #ff7b00;
  border-radius: 15px;
  
  border: none;
  cursor: pointer;
}

#sidebar-menu2 a:hover,
#sidebar-menu2 button:hover {
  background-color: #fc9c43;
}

#sidebar-profile2 h5{
  color: #000000;
  
}

</style>
