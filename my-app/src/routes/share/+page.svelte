<script>
  import "bootstrap/dist/css/bootstrap.min.css";
  import Footer from "../../libs/Footer.svelte";
  import Navbar from "../../libs/Navbar.svelte";
  import Sidebar from "../../libs/Sidebar.svelte";
  import { page } from "$app/stores";
  import { onMount } from "svelte";

  let data;
  onMount(async () => {
    data = localStorage.getItem("token");
    if (!data) {
      window.location.href = "/login";
    }
  });

  let username = $page.url.searchParams.get("username");

  let category;
  let file;
  let url;
  let subject;
  let description;

  function handleCategory() {
    category = category;
  }

  async function sharePost() {
    const res = await fetch(
      `http://127.0.0.1:5173/user/sharePost/${username}`,
      {
        method: "POST",
        body: JSON.stringify({
          post_category: category,
          post_url: url,
          // post_file: file,
          post_subject: subject,
          post_description: description,
        }),
      }
    );
    const item = await res.json();
  }
</script>

<Navbar {username} />
<!-- <Sidebar/> -->
<br /><br />
<div
  class="container-fluid py-5 bg-dark-subtle shadow"
  id="shareForm"
  style="border-radius: 20px;"
>
  <div>
    <div class="mb-3">
      <label for="exampleFormControlSelect1" class="form-label">Category</label>
      <select
        bind:value={category}
        on:change={handleCategory}
        class="form-control"
        id="exampleFormControlSelect1"
      >
        <option>Technology</option>
        <option>Business</option>
        <option>Science</option>
        <option>Arts</option>
        <option>Sports</option>
      </select>
    </div>
    <label for="formFileLg" class="form-label">File</label>
    <input
      class="form-control form-control-l"
      bind:value={file}
      id="formFileLg"
      type="file"
    />
    <label for="formFileLg" class="form-label">or Link</label>
    <input
      class="form-control form-control-l"
      bind:value={url}
      id="formFileLg"
      type="url"
      placeholder="example.com"
    />
  </div>
  <div class="mb-3">
    <label for="exampleFormControlInput1" class="form-label">Subject</label>
    <input
      type="text"
      class="form-control"
      id="exampleFormControlInput1"
      placeholder=""
      bind:value={subject}
    />
  </div>
  <div class="mb-3">
    <label for="exampleFormControlTextarea1" class="form-label">Textarea</label>
    <textarea
      class="form-control"
      bind:value={description}
      id="exampleFormControlTextarea1"
      rows="3"
    />
  </div>
  <button
    class="btn btn-sm btn-primary btn-lg"
    on:click={sharePost}
    type="button">Share</button
  >
</div>
<br />
<Footer />

<style>
  #shareForm {
    width: 550px;
    /* position: relative;
          top: -600px;
          left:50%;
          transform: translateX(-50%);
          margin-left: 60px;
          overflow: hidden; */
  }
</style>
