<template>
  <div style="text-align:center !important; ">
     <div id="sidebar-header">
    <nav class="navbar navbar-expand-lg navbar-light ">
  <a class="navbar-brand" href="#">CookVerse</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavDropdown">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link" href="#"><router-link to="/HomePage">Feed</router-link><span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#"><router-link to="/minha-conta">Minha Conta</router-link></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#"><router-link to="/">Minhas Curtidas</router-link></a>
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
        <h5>Olá {{usuario.nome}}, seja bem vindo ao Cookverse!</h5>
        <hr>
      </div>
      <div id="sidebar-menu">
        <router-link to="/HomePage">Feed</router-link>
        <router-link to="/minha-conta">Minha Conta</router-link>
        <router-link to="/">Minhas Curtidas</router-link>

        <button @click="sair">Sair</button>
      </div>
      
    </div>


      <div id="sidebar2">
      
      <div id="sidebar-profile2">
        <a href=""><img src="" alt=""></a>
        <h5>Receitas mais curtidas</h5>
         <hr>
          <receitas-curtidas ref="receitasCurtidasComponent"/>

       
      </div>
      <div id="sidebar-menu2">
        

        
      </div>
      
    </div>
    <div class="feed-container" >

    <div class="container" id="fd">
     
   <div id="headerButtons">
  <button class="btn-main" :class="{ 'btn-active': botaoAtivo === 'Feed' }" @click="loadFeed('Feed')">Receitas</button>
<button class="btn-main" :class="{ 'btn-active': botaoAtivo === 'Meu Feed' }" @click="loadFeed('Meu Feed')">Minhas receitas</button>

  </div>



      <div class="container" style="padding-bottom:px; padding-top: 50px"> 
        <criar-postagem @novaPostagemCriada="adicionarNovaPostagem"></criar-postagem>
      </div>
<div id="headerTitle" class="mb-3" style="padding-top: 50px; display: flex; align-items: center;">
  <div class="input-group" style="flex-grow: 1;">
    <input
      type="text"
      v-model="termoPesquisa"
      class="form-control"
      placeholder="Pesquisar"
    />
    
  </div>
  <button id="refresh" class="btn btn-circle btn-secondary" @click="refreshFeed">
    <Refresh/>
  </button>
</div>
            <div v-if="showIframe" class="overlay">
              <iframe :class="{'success': showIframe }" 
                id="load"
                src="https://lottie.host/embed/4a40d72c-2547-4f2a-909c-2044e6b7717e/xIffzuE3W0.json"
              ></iframe>
            </div>

      <div v-if="postagens.length === 0">
        <p>Não há nenhuma postagem para ser visualizada</p>
      </div>
      
      <div v-if="feedAtivo === 'Feed'">
        <div class="post" v-for="postagem in postagens" :key="postagem.id">
           <menu-icon @click="verDetalhes(postagem.id)" v-if="botaoAtivo === 'Meu Feed'" style="float:right" id="detalhes"  />
   
           <div v-if="postSelecionado !== null">
           <details-modal
        v-show="mostrarModal"
        :postSelecionado="postSelecionado"
        @close="mostrarModal = false"
        @postagemExcluida="atualizarListaPostagens"
        @postagemEditada="atualizarListaPostagensEditada"
      ></details-modal>
</div>
        <div class="post-header">
          <div>
            <h5>{{ postagem.titulo }}</h5>
            
       
            <p>{{ formatarData(postagem.datahora_postagem) }}</p>
           
          </div>
        </div>
        <hr>
        <div class="post-content">
          <img :src="postagem.url_img" width="100%" alt="">
          <br><br>
          <p>{{ postagem.texto }}</p>
        </div>
        <div id="autor">
          <p>Criado por: {{postagem.nome_autor}}</p>
<hr>
        <div v-for="comentario in postagem.comentarios" :key="comentario.id" class="comentario">
    <p>{{ comentario.texto }}</p>

  </div>
        <div class="post-footer">







   <div class="input-group" style=" margin-right:50px">
    <input
      type="text"
      v-model="novoComentario.texto"
      class="form-control"
      placeholder="Adicionar comentário"
    />
    <button @click="adicionarComentario(postagem.id)" class="btn-main" style="border-radius: 0">Enviar</button>
  </div>




<div id="curtida-group" style="display:flex; ">
        <button id="curtida" @click="curtirPostagem(postagem)" :disabled="postagem.curtido" class="btn btn-circle btn-orange">
          <Like/>
        </button>

        <span>{{ postagem.num_curtidas }}</span>
        </div>
      </div>
      </div>
      </div>
      </div>
      <div v-else-if="feedAtivo === 'Meu Feed'">
        <postagens-usuario :postagens="postagens"></postagens-usuario>
        
      </div>

      
      </div>
    </div>

  </div>
</template>

<script>
import api from "./api";
import CriarPostagem from "./CriarPostagem.vue";
import PostagensUsuario from "./PostagensUsuario.vue";
import ReceitasCurtidas from "./ReceitasCurtidas.vue";
import MenuIcon from 'vue-material-design-icons/DotsHorizontal.vue';
import Like from 'vue-material-design-icons/ThumbUpOutline.vue';
import Refresh from 'vue-material-design-icons/Refresh.vue';

import DetailsModal from "./DetailsModal.vue";
import { jwtDecode } from "jwt-decode";
import { useToast } from "vue-toastification";
const toast = useToast();

export default {
  name: "HomePage",
  components: {
    CriarPostagem,
    PostagensUsuario,
    ReceitasCurtidas,
    DetailsModal,
    Like,
    Refresh,
    MenuIcon
  },
  data() {
    return {
      user: '',
      id: '',
      mostrarModal: false,
      postSelecionado: null,
      showIframe: false,
      postagens: [],
      novoComentario: {
      texto: '',
    },
      botaoAtivo: 'Feed',
      termoPesquisa: "",
      usuario: {
        nome: "Igor Santos",
        idade: 25,
        email: "igor@gmail.com"
      },
      userId: null,
      feedAtivo: 'Feed'
    };
  },
 
  async created() {
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error("Não tem token");
    } else {
      const decToken = jwtDecode(token);
      this.userId = decToken.sub; 
      console.log(this.userId)
      await this.getUserData(this.userId);
    }
  },

  mounted() {
    this.getPostagens();
  },
  methods: {
     async loadFeed(feed) {
      if (feed === 'Feed') {
        await this.getPostagens();
      } else if (feed === 'Meu Feed') {
        await this.getPostagensUsuario();
        console.log(feed)
      }
      this.botaoAtivo = feed; 
    },
    async adicionarNovaPostagem(novaPostagem) {
    try {
      this.postagens.push(novaPostagem);

      this.refreshFeed(this.botaoAtivo);


      this.$router.push({ path: "/HomePage" });
    } catch (error) {
      console.error(error);
    }
  },
    
    async adicionarComentario(idPostagem) {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error("Usuário não autenticado.");
      return;
    }

    const comentario = this.novoComentario.texto;
    if (!comentario.trim()) {
      toast.error("Insira uma mensagem");
      return;
    }

    const requestBody = {
      texto: comentario,
      nome_autor: this.usuario.nome, 
    };

    await api.post(`/adicionar-comentario/${idPostagem}`, requestBody, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    await this.getPostagens();

    this.novoComentario.texto = '';

    toast.success("Comentário adicionado com sucesso!");
  } catch (error) {
    console.error(error);
    toast.error("Erro ao adicionar comentário.");
  }
}
,
async atualizarListaPostagens(idExcluido) {
      try {
        this.postagens = this.postagens.filter(postagem => postagem.id !== idExcluido);
      } catch (error) {
        console.error('Erro ao atualizar lista de postagens após exclusão:', error);
      }
    },
    async atualizarListaPostagensEditada() {
  this.getPostagensUsuario();
},

  async getPostagensUsuario() {
  try {
    const response = await api.get(`/postagens?id=${this.userId}`);
    this.postagens = response.data.postagens; 
  } catch (error) {
    console.error(error);
    toast.error("Erro ao carregar postagens do usuário.");
  }
},
    async getPostagens() {
  this.showIframe = true;
  try {
    const response = await api.get("/postagens");
    const postagens = response.data.postagens;
    var comentarios = ''
    for (const postagem of postagens) {
      const comentariosResponse = await api.get(`/buscar-comentario/${postagem.id}`);
      comentarios = comentariosResponse.data.comentarios;
    }
     console.log(comentarios)
     console.log(postagens)
    this.postagens = [...postagens];
    setTimeout(() => {
      this.showIframe = false;
    }, 1500);
  } catch (error) {
    console.log(error);
    this.showIframe = false;
  }
},

    refreshFeed(feed) {
      try{
        this.getPostagens();
        if (feed === 'Feed') {
         this.getPostagens();
      } else if (feed === 'Meu Feed') {
         this.getPostagensUsuario();
      }
      this.botaoAtivo = feed; 

      }catch(error){
        console.log(error)
      }
    },
    async getUserData(userId) {
      try {
        const response = await api.get(`obter_usuarios?id=${userId}`);
        this.usuario = response.data.usuario;
        console.log(this.usuario.nome)
        localStorage.setItem("user", JSON.stringify(this.usuario));
      } catch (error) {
        console.error(error);
      }
    },
    async getCurtidas(){

    },
    formatarData(data) {
      const dataObj = new Date(data);
      return `${dataObj.toLocaleDateString()} ${dataObj.toLocaleTimeString()}`;
    },
    verDetalhes(index) {
    console.log('Índice selecionado:', index);

    const postagemSelecionada = this.postagens.find(postagem => postagem.id === index);

    if (postagemSelecionada) {
      console.log('Postagem selecionada:', postagemSelecionada);
      this.mostrarModal = true;
      this.postSelecionado = postagemSelecionada;
    } else {
      console.error('Postagem não encontrada');
    }
  },
    async curtirPostagem(postagem) {
      try {
        const requestBody = { usuario_id: this.userId }; 
        await api.post(`/postagens/curtidas/${postagem.id}`, requestBody);
        
        postagem.num_curtidas++;
        this.$refs.receitasCurtidasComponent.carregarReceitasCurtidas();
        //postagem.curtido = true;
        
      } catch (error) {
        console.error(error);
      }
    },
    sair() {
      this.$router.push({
        path: "/LoginPage",
      });
      localStorage.removeItem('access_token');
    },
    
    
  },
};
</script>

<style scoped>

.feed-container {
  max-height: calc(100vh - 60px); 
  overflow-y: auto; 
}

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

  .post-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}





.post-footer button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
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

.post-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.btn-circle {
  padding:5px;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: #ff7b00;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border: none;
  cursor: pointer;
}

.btn-circle:hover {
  background-color: #fc9c43;
}

#curtida {
  margin-right: 15px !important;
}

.post {
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  margin-bottom: 20px;
  padding: 15px;
  border-radius: 8px;
}

.post-header h5 {
  margin: 0;
  color: #333;
  text-align: left;
}

.post-header p {
  text-align: left;
  font-size: 15px;
}

.post-content {
  margin-bottom: 10px;
  text-align: left;
}

.post-text {
  text-align: left;
  margin: 0;
}

.post-footer {
  display: flex;
  align-items: center;
}

.post-footer p {
  text-align: left !important;
  float: left !important;
  justify-content: flex-start !important;
}

.btn-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #ff7b00;
  color: white;
  border: none;
  cursor: pointer;
  margin-right: 10px;
}

.btn-circle:hover {
  background-color: #fc9c43;
}

.no-posts {
  text-align: center;
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  border-radius: 8px;
}

#autor{
  justify-content: flex-start !important;
  text-align: left;
  font-style: italic;
}

#fd{
    border-left: 1px solid #ccc !important;
  border-right: 1px solid #ccc !important;
}

#refresh{
  margin-right: 0px;
  margin-left: 15px;
}

.btn-main {
  background-color: #ff7b00;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  margin-right: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-main:hover,
.btn-main:focus {
  background-color: #fc9c43;
  outline: none;
}

.btn-active {
  background-color: #fc9c43;
  color: white;
}

#headerButtons{
  margin-top: 20px;
}
.btn-circle-details{
 
  color: white;
  border: none;
  cursor: pointer;
  margin-right: 10px;
}
.btn-circle-details:hover{
 background-color: #ff7b00;
}

#detalhes:Hover{
  color: #fc9c43;
  background-color:rgb(255, 255, 255) ;
  border-radius: 50px;

}
</style>
