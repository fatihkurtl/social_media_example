<script>
  import "bootstrap/dist/css/bootstrap.min.css";
  import Navbar from "../../libs/Navbar.svelte";
  import Footer from "../../libs/Footer.svelte";
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

  let bio = [];

  async function userBio() {
    // const jwt_token = localStorage.getItem("jwt_token");
    const res = await fetch(
      `http://127.0.0.1:5173/user/profileBio/${username}`,
      {
        method: "POST",
        headers: {
          // Authorization: `Bearer ${jwt_token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user: username,
          // token: jwt_token,
          status: true,
        }),
      }
    );
    const data = await res.json();
    // console.log(data);
    bio = data.bio[0];
  }
  userBio();

  let profilePosts = [];

  async function userProfile() {
    // const jwt_token = localStorage.getItem("jwt_token");
    const res = await fetch(`http://127.0.0.1:5173/user/profile/${username}`, {
      method: "POST",
      headers: {
        // Authorization: `Bearer ${jwt_token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user: username,
        // token: jwt_token,
        status: true,
      }),
    });
    const item = await res.json();
    profilePosts = item.post;
  }
  userProfile();

  async function postStat(id, stat) {
    const res = await fetch(`http://127.0.0.1:5173/post_status`, {
      method: "POST",
      body: JSON.stringify({ id: id, stat: stat }),
    });
    const postsInfo = await res.json();
  }

  let followerCount;
  async function followerStat() {
    const res = await fetch(`http://127.0.0.1:5173/userFollowers/${username}`, {
      method: "POST",
      body: JSON.stringify({ status: 201, info: true }),
    });
    const followerInfo = await res.json();
    followerCount = followerInfo.msg.length;
  }
  followerStat();
  async function sharedPosts(id) {
    const res = await fetch(`http://127.0.0.1:5173/shared/posts/${username}`, {
      method: "POST",
      body: JSON.stringify({ id: id }),
    });
    const postsInfo = await res.json();
    console.log(postsInfo.msg);
  }
</script>

<Navbar {username} />
<!-- <Sidebar/> -->
<br />
<div class="container shadow">
  <div class="header">
    <div class="row">
      <div class="col-md-2">
        <img
          src={bio[5]}
          class="profile-img"
          style="height:130px; width: 130px;"
          alt="Profile_Image"
        />
      </div>
      <div class="col-md-10">
        <div class="profile-info">
          <h2 class="profile-name">{bio[1]} {bio[2]}</h2>
          <p class="profile-username">@{bio[3]}</p>
        </div>
        <div class="header-stats">
          <div class="stat">
            <p class="stat-number">{profilePosts.length}</p>
            <p class="stat-label">Tweets</p>
          </div>
          <div class="stat">
            <p class="stat-number">{followerCount}</p>
            <p class="stat-label">Followers</p>
          </div>
          <div class="stat">
            <p class="stat-number">{followerCount}</p>
            <p class="stat-label">Following</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="content row">
    {#each profilePosts as posts}
      <div class="col-md-4">
        <div class="col">
          <div class="card h-100">
            <img src={posts[3]} class="card-img-top" alt="..." />
            <div class="card-body bg-dark-subtle">
              <h5 class="card-title">{posts[4]}</h5>
              <p class="card-text">{posts[5]}</p>
            </div>
            <div class="col-sm-12 bg-dark-subtle text-center">
              <span
                id="like"
                class="btn btn-none badge text-secondary col-sm-2"
                style="text-decoration: none;"
                on:click={postStat(posts[0], "like")}
                on:keypress={postStat(posts[0], "like")}
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
                <small class="text-muted badge">{posts[6]}</small>
              </span>

              <span
                id="dislike"
                class="btn btn-none badge text-secondary col-sm-2"
                style="text-decoration: none;"
                on:click={postStat(posts[0], "dislike")}
                on:keypress={postStat(posts[0], "dislike")}
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
                <small class="text-muted badge">{posts[7]}</small>
              </span>

              <span
                id="share"
                class="btn badge text-secondary col-sm-2"
                style="text-decoration: none;"
                on:click={sharedPosts(posts[0], "share")}
                on:keypress={sharedPosts(posts[0], "share")}
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
              <span
                id="trash"
                class="btn badge text-secondary col-sm-2"
                style="text-decoration: none;"
                on:click={postStat(posts[0], "delete")}
                on:keypress={postStat(posts[0], "delete")}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-trash3-fill"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"
                  />
                </svg>
              </span>
            </div>
            <div class="card-footer bg-dark-subtle">
              <small class="text-primary-emphasis row col-sm">{posts[8]}</small>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>

<Footer />

<style>
  .container {
    background-color: #f8f9fa;
    padding: 50px;
  }

  .header {
    border-bottom: 1px solid #e1e8ed;
    padding-bottom: 20px;
    margin-bottom: 20px;
  }

  .profile-img {
    width: 80px;
    height: auto;
    border-radius: 50%;
    margin-right: 20px;
  }

  .profile-info {
    display: flex;
    align-items: center;
  }

  .profile-name {
    font-size: 24px;
    font-weight: bold;
    margin-right: 10px;
    color: #14171a;
  }

  .profile-username {
    font-size: 20px;
    font-weight: normal;
    color: #657786;
  }

  .header-stats {
    display: flex;
    margin-top: 10px;
  }

  .stat {
    flex: 1;
    text-align: center;
  }

  .stat-number {
    font-size: 18px;
    font-weight: bold;
    color: #14171a;
    margin-bottom: 5px;
  }
  .stat-label {
    font-size: 14px;
    color: #657786;
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
  #trash:hover {
    color: #ffc107 !important;
  }
</style>
