<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Input all your tasks and let us assist with the organization
    </p>
    <input type="text" v-model="task" @keypress.enter="addTask" placeholder="Write a task or goal here..." />
    <ul>
      <li v-for="(item, index) in items" :key="index">
        <span :class="{ 'completed': item.completed }">{{ item.text }}</span>
        <button @click="toggleComplete(index)">Concluir</button>
        <button @click="deleteTask(index)">Deletar</button>
      </li>
    </ul>
  </div>
</template>


<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      task: '',
      items: []
    };
  },
  props: {
    msg: String
  },
  methods: {
    addTask() {
      let task = this.task.trim();

      if (task) {
        this.items.push({ text: task, completed: false });
        this.task = '';
      }
    },
    toggleComplete(index) {
      this.items[index].completed = !this.items[index].completed;
    },
    deleteTask(index) {
      this.items.splice(index, 1);
    }
  }
};

</script>

<style scoped>
input{
  height: 50px;
  width: 500px;
  margin: 10px;
  padding: 10px;
  font-size: 30px;
  font-family: "Poppins", sans-serif;

}

li{
  list-style: none;
  height: 50px;
  width: 500px;
  margin: 10px;
  padding: 10px;
  font-size: 30px;
  font-family: "Poppins", sans-serif;
  background-color: aliceblue;
  display: flex;

}


.completed {
  text-decoration: line-through;
}


@media only screen and (max-width: 600px) {
  input, li{
    height: 20px;
    width: 250px;
    margin: 10px;
    padding: 10px;
    font-size: 15px;
    font-family: "Poppins", sans-serif;

  }

}

</style>
