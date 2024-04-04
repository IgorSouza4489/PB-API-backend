<template>
  <div class="modal-overlay">
    <div id="container">
      <div id="modal">
        <div class="modal-header">
          <h2>{{postSelecionado.titulo}}</h2>
          <button class="btn-close" @click="$emit('close')">
            <MenuIcon size="24px" />
          </button>
        </div>
        <div class="modal-content">
          <p><strong>Autor:</strong> {{ postSelecionado.nome_autor }}</p>
          <div class="form-group">
            <label for="titulo">Título:</label>
            <input type="text" id="titulo" v-model="editedPost.titulo" />
          </div>
          <div class="form-group">
            <label for="texto">Texto:</label>
            <textarea id="texto" rows="4" v-model="editedPost.texto"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-excluir" @click="excluirPostagem">Excluir</button>
          <button class="btn-salvar" @click="salvarEdicao">Salvar</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import MenuIcon from 'vue-material-design-icons/Close.vue';
import api from "./api";
import { useToast } from "vue-toastification";
const toast = useToast();

export default {
  components: {
    MenuIcon,
  },
  props: {
    postSelecionado: Object,
  },
  data() {
    return {
      editedPost: {
        titulo: '',
        texto: '',
      },
    };
  },
  mounted() {
    this.editedPost.titulo = this.postSelecionado.titulo;
    this.editedPost.texto = this.postSelecionado.texto;
  },
  methods: {
   async salvarEdicao() {
    try {
      const response = await api.patch(`/postagens/${this.postSelecionado.id}`, this.editedPost);
      console.log('Resposta da edição:', response.data);
      this.$emit('close');
      toast.success('Postagem editada com sucesso!');
      this.$emit('postagemEditada', this.postSelecionado.id);
    } catch (error) {
      console.error('Erro ao salvar edição:', error);
      toast.error('Erro ao salvar edição. Tente novamente mais tarde.');
    }
  },
    async excluirPostagem() {
      try {
        const response = await api.delete(`/postagens/${this.postSelecionado.id}`);
        console.log('Resposta da exclusão:', response.data);
        this.$emit('close');
        toast.warning('Postagem excluída');

        // Atualizar a lista de postagens após a exclusão
        this.$emit('postagemExcluida', this.postSelecionado.id);
      } catch (error) {
        console.error('Erro ao excluir postagem:', error);
      }
    },
  },
};
</script>


<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(223, 223, 223, 0.3) !important;
}

#container {
  width: 100%;
  display: flex;
  justify-content: center;
}

#modal {
  background-color: #fff;
  width: 400px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-content {
  margin-bottom: 20px;
}

.form-group {
  margin: 10px;
}

label {
  font-weight: bold;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
}

.btn-excluir,
.btn-salvar {
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-excluir {
  background-color: #f44336;
  color: #fff;
  margin-right: 10px;
}

.btn-salvar {
  background-color: #4caf50;
  color: #fff;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
}
</style>
