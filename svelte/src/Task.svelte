<script>
  import { api } from "./api.js";

  const STATUS_CHOICES = ["pending", "completed"];

  // These are the properties of the component.
  export let id;
  export let projectId;
  export let parentId;
  export let order;
  export let shortDescription;
  export let longDescription;
  export let status;

  async function handleStatusChange(event) {
    const newStatus = event.target.value;
    const payload = {
      id: id,
      status: newStatus,
    };
    const responseJson = await api("/api/task/update/status", payload);
    if (responseJson.error) {
      console.error(responseJson.error)
      // TODO: Display a message to the user.
      return;
    }
    status = newStatus;
  }
</script>

<style>
  div {
    padding: 15px;
  }

  h2 {
    margin-top: 0;
  }

  select {
    margin-bottom: 0;
  }

  div + div {
    margin-top: 15px;
  }

  .status-pending {
    background-color: #A9CAEF;
  }

  .status-completed {
    background-color: #BFDF7F;
    opacity: 50%;
  }

  .status-blocked {
    background-color: orange;
  }

  .status-obsolete {
    background-color: #F0F0F0;
    opacity: 50%;
  }

  .status-nonblocking {
    background-color: #F0F0F0;
  }

  .status-failed {
    background-color: #EC6484;
    opacity: 50%;
  }
</style>

<div class="status-{status}">
  <h2>
    {#if status === "completed"}
      <s>{shortDescription}</s>
    {:else}
      {shortDescription}
    {/if}
  </h2>
  {#if longDescription !== null}
    <p>{longDescription}</p>
  {/if}

  <select on:change={handleStatusChange}>
    <option name="{status}">{status}</option>
    {#each STATUS_CHOICES as statusChoice}
      {#if status !== statusChoice}
        <option name="{statusChoice}">{statusChoice}</option>
      {/if}
    {/each}
  </select>
</div>
