<template>
  <div>
    
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

  },
  methods: {
   
  },
};
</script>


<style scoped>

</style>
