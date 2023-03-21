<script>
  import "bootstrap/dist/css/bootstrap.min.css";
  import Navbar from "../../libs/Navbar.svelte";
  import Sidebar from "../../libs/Sidebar.svelte";
  import Footer from "../../libs/Footer.svelte";
  import { page } from "$app/stores";
  import { onMount } from "svelte";

  let username = $page.url.searchParams.get("username");

  let data;
  onMount(async () => {
    data = localStorage.getItem("token");
    if (!data) {
      window.location.href = "/login";
    }
  });
  async function postStat(id, stat) {
    const res = await fetch(`http://127.0.0.1:5173/post_status`, {
      method: "POST",
      body: JSON.stringify({ id: id, stat: stat }),
    });
    const postsInfo = await res.json();
    console.log(postsInfo)
  }

  async function sharedPosts(id) {
    const res = await fetch(`http://127.0.0.1:5173/shared/posts/${username}`, {
      method: "POST",
      body: JSON.stringify({ id: id }),
    });
    const postsInfo = await res.json();
    console.log(postsInfo.msg);
  }

  let get_post = [];
  async function shared_posts(id, stat) {
    const res = await fetch(
      `http://127.0.0.1:5173/show_shared_posts/${username}`,
      {
        method: "POST",
        body: JSON.stringify({ status: 200, info: true }),
      }
    );
    const posts = await res.json();
    get_post = posts.msg;
    console.log(get_post);
  }
  shared_posts();

  async function deleteFriend(friend) {
    const res = await fetch(`http://127.0.0.1:5173/deleteFriend/${username}`, {
      method: "POST",
      body: JSON.stringify({ info: true, msg: friend }),
    });
    const status = await res.json();
    alert(status.msg);
  }

  // async function shared_stat() {
  //   const res = await fetch(`http://127.0.0.1:5173/number_of_shared`, {
  //     method: "POST",
  //     body: JSON.stringify({ subject: ''}),
  //   });
  //   const stat = await res.json();
  //   console.log(stat);
  // }
  // shared_stat();
</script>

<Navbar {username} />
<!-- <Sidebar/> -->

<br />

<div class="container shadow">
  <div class="content row">
    {#each get_post as item}
      <div class="col-md-4">
        <div class="col">
          <div class="card h-100">
            <img src={item[4]} class="card-img-top" alt="..." />
            <div class="card-body bg-dark-subtle">
              <a
                href="/user_account?username={item[2]}"
                class="badge text-primary-emphasis"
                style="text-decoration: none;">@{item[2]}</a
              >
              <button
                on:click={deleteFriend(item[1])}
                type="button"
                class="btn btn-outline-danger"
                style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-person-dash-fill"
                  viewBox="0 0 16 16"
                >
                  <path
                    fill-rule="evenodd"
                    d="M11 7.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5z"
                  />
                  <path
                    d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"
                  />
                </svg>
              </button>
              <h5 class="card-title">{item[5]}</h5>
              <p class="card-text">{item[6]}</p>
            </div>
            <div class="col-sm-12 bg-dark-subtle text-center">
              <span
                id="like"
                class="btn btn-none badge text-secondary col-sm-3"
                style="text-decoration: none;"
                on:click={postStat(item[0], "like")}
                on:keypress={postStat(item[0], "like")}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-heart-fill"
                  viewBox="0 0 16 16"
                >
                  <path
                    fill-rule="evenodd"
                    d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"
                  />
                </svg>
                <small class="text-muted badge">{item[7]}</small>
              </span>

              <span
                id="dislike"
                class="btn btn-none badge text-secondary col-sm-3"
                style="text-decoration: none;"
                on:click={postStat(item[0], "dislike")}
                on:keypress={postStat(item[0], "dislike")}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-heartbreak-fill"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M8.931.586 7 3l1.5 4-2 3L8 15C22.534 5.396 13.757-2.21 8.931.586ZM7.358.77 5.5 3 7 7l-1.5 3 1.815 4.537C-6.533 4.96 2.685-2.467 7.358.77Z"
                  />
                </svg>
                <small class="text-muted badge">{item[8]}</small>
              </span>

              <span
                id="share"
                class="btn badge text-secondary col-sm-3"
                style="text-decoration: none;"
                on:click={sharedPosts(item[0], "share")}
                on:keypress={sharedPosts(item[0], "share")}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-share-fill"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.499 2.499 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5z"
                  />
                </svg>
                <small class="text-muted badge" />
              </span>
            </div>
            <div class="card-footer bg-dark-subtle">
              <pre class="text-primary-emphasis row col-sm">{item[9]}</pre>
              <pre class="text-muted badge">Shared User: @{item[1]}</pre>
            </div>
          </div>
        </div>
      </div>
    {/each}
    <!-- <div class="list-group col-md-4">
      <a href="/" class="list-group-item list-group-item-action">aaaaaa</a>
    </div> -->
  </div>
</div>

<Footer />

<style>
  .container {
    background-color: #f8f9fa;
    padding: 50px;
  }
  .btn {
    border: none !important;
  }
  #like:hover {
    color: red !important;
  }
  #dislike:hover {
    color: #6610f2 !important;
  }
  #share:hover {
    color: #0d6efd !important;
  }
</style>
