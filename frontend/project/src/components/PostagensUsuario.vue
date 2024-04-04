<template>
  <div>
    <div v-if="postagens.length === 0">
      <p>Não há nenhuma postagem para ser visualizada</p>
    </div>
    <div v-else>
      <div class="post" v-for="postagem in postagens" :key="postagem.id">
       <button v-if="feedAtivo === 'Meu Feed'" @click="editarPostagem(postagem)">Editar</button>
        <button v-if="feedAtivo === 'Meu Feed'" @click="excluirPostagem(postagem.id)">Excluir</button>

        <div class="post-header">
          <div>
            <h5>{{ postagem.titulo }}</h5>
            <p>{{ formatarData(postagem.datahora_postagem) }}</p>
          </div>
        </div>
        <hr>
        <div class="post-content">
          <p>{{ postagem.texto }}</p>
        </div>
        <div id="autor">
          <p>Autor: {{postagem.nome_autor}}</p>
          
          <div class="post-footer">
            <span>{{ postagem.num_curtidas }} curtidas</span>
            
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
const toast = useToast();

export default {
  name: "PostagensUsuario",
  components: {},
  props: {
    postagens: Array,
  },
  data() {
    return {};
  },
  async created() {
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error("Token não encontrado.");
      return;
    }
  },
  methods: {
    formatarData(data) {
      const dataObj = new Date(data);
      return `${dataObj.toLocaleDateString()} ${dataObj.toLocaleTimeString()}`;
    },
    editarPostagem(postagem) {
      // Implemente a lógica de edição aqui
      console.log("Editar postagem:", postagem);
    },
    excluirPostagem(postagemId) {
      // Implemente a lógica de exclusão aqui
      console.log("Excluir postagem ID:", postagemId);
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
  width: 20px;
  height: 20px;
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
</style>

