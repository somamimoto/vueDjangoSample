<template>
    <div>
      <h1><a href="http://localhost:8080">Todo List</a></h1>
      <ul>
        <li v-for="todo in todos" :key="todo.id">
          {{ todo.title }} - {{ todo.completed ? 'Completed' : 'Not Completed' }}
          <button @click="editTodo(todo)">Edit</button>
          <button @click="deleteTodo(todo.id)">Delete</button>
        </li>
      </ul>

      <h2>{{ isEditing ? 'Edit' : 'Add' }} Todo</h2>
      <form @submit.prevent="isEditing ? updateTodo() : addTodo()" novalidate><!-- novalidate で browserのdefault validationを無効化 => for test-->
        <input v-model="form.title" placeholder="Title" required />
        <textarea v-model="form.description" placeholder="Description"></textarea>
        <label>
          <input type="checkbox" v-model="form.completed" />
          Completed
        </label>
        <button type="submit">{{ isEditing ? 'Update' : 'Add' }}</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </template>

  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        todos: [],  // 取得したTodoデータを格納する配列
        form: {
          id: null,
          title: '',
          description: '',
          completed: false
        },
        isEditing: false,
        errorMessage: '',  // data property for error message
      };
    },
    mounted() {
      this.fetchTodos();  // コンポーネントがマウントされたときにデータを取得するメソッドを呼び出す
    },
    methods: {
      async fetchTodos() {
        try {
          // DjangoのAPIからデータを取得する
          const response = await axios.get('http://localhost:8000/api/todos/');
          this.todos = response.data;  // 取得したデータをtodosに格納する
          this.resetForm();
        } catch (error) {
          console.error('Error fetching todos:', error);
        }
      },
      async addTodo() {
        try {
          const response = await axios.post('http://localhost:8000/api/todos/', this.form);
          this.todos.push(response.data);
          this.resetForm();
        } catch (error) {
          // console.error('Error adding todo:', error);
          this.errorMessage = 'Error adding todo: ' + error.response.data.detail || 'An error occurred';
        }
      },
      editTodo(todo) {
        this.isEditing = true;
        this.form = { ...todo };  // todoのcloneをthis.formに設定する. (スプレッド構文 (...)を使い、todoオブジェクトのすべてのプロパティをthis.formにコピーしている)
      },
      async updateTodo() {
        try {
          const response = await axios.put(`http://localhost:8000/api/todos/${this.form.id}/`, this.form);
          const index = this.todos.findIndex(todo => todo.id === response.data.id);
          this.todos.splice(index, 1, response.data); // リストを更新
          this.resetForm();
        } catch (error) {
          // console.error('Error updating todo:', error);
          this.errorMessage = 'Error updating todo: ' + error.response.data.detail || 'An error occurred';
        }
      },
      async deleteTodo(id) {
        try {
          await axios.delete(`http://localhost:8000/api/todos/${id}/`);
          this.todos = this.todos.filter(todo => todo.id !== id);
        } catch (error) {
          // console.error('Error deleting todo:', error);
          this.errorMessage = 'Error deleting todo: ' + error.response.data.detail || 'An error occurred';
        }
      },
      resetForm() {
      this.form = {
        id: null,
        title: '',
        description: '',
        completed: false
      };
      this.isEditing = false;
      this.errorMessage = '';
    }
    },
  };
  </script>
