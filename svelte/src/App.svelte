<script>
  import { onMount } from 'svelte';
  import { api } from "./api.js";
  import Task from './Task.svelte';

  let id;
  let name;
  let description;
  let archived;
  let loading = true;
  let tasks = [];

  onMount(async () => {
    const response = await fetch("/api/project/get?id=1");
    const data = await response.json();
    // Svelte will automatically update the UI when the tasks are assigned.
    ({id, name, description, archived, tasks} = data);
    loading = false;
  });

  async function handleNewTask(event) {
    if (event.keyCode === 13) {
      const description = event.target.value.trim();
      const payload = {
          description: description,
          order: tasks.length,
          parentId: null,
          projectId: id,
      };
      const newTask = await api("/api/task/create", payload);
      event.target.value = "";
      if (newTask.error) {
        console.error(newTask.error);
        // TODO: Display a message to the user.
        return;
      }

      // Svelte will automatically update the UI when a new task is appended.
      // However, updates are only triggered on re-assignment, which is why it
      // is written like this and not `tasks.append(newTask)`.
      tasks = [...tasks, newTask];
    }
  }
</script>

<style>
  /* Styles are scoped to the component and won't affect other components. */
  label, input {
    display: inline-block;
  }

  main {
    width: 62rem;
    margin: 0 auto;
  }

  label {
    margin-right: 5px;
  }

  #new-task-form {
    text-align: center;
  }

  .message {
    font-size: 24px;
    text-align: center;
  }
</style>

<svelte:head>
  <title>[svelte] {name}</title>
</svelte:head>

<main>
  <div id="new-task-form">
    <label for="new-task">Create a new task: </label>
    <input type="text" id="new-task" on:keyup={handleNewTask}>
  </div>

  {#if loading}
    <p class="message">Loading...</p>
  {:else}
    {#each tasks as task}
      <Task {...task}></Task>
    {:else}
      <p class="message">No tasks yet</p>
    {/each}
  {/if}
</main>
