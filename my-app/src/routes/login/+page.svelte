<script>
  import "bootstrap/dist/css/bootstrap.min.css";
  import Navbar from "../../libs/Navbar.svelte";
  import Footer from "../../libs/Footer.svelte";
  import { createEventDispatcher } from "svelte";
  import { onMount } from "svelte";

  // import {setJWT, getJWT} from './jwt';
  // import jwt from 'jsonwebtoken';

  const dispatch = createEventDispatcher();
  function handleClick() {
    dispatch("myEvent", { message: username });
  }

  let remember_me = false;
  const checkbox = () => {
    remember_me == true ? (remember_me = false) : (remember_me = true);
  };
  let username;
  let password;

  let userName_alert = "";
  let password_alert = "";

  let token;

  async function doPostLogin() {
    if (username && password) {
      const jwt_token = localStorage.getItem("jwt_token");
      const res = await fetch(`http://127.0.0.1:5173/auth`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${jwt_token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_name: username,
          user_password: password,
        }),
      });
      const item = await res.json();
      console.log(item);
      if (item.access_token) {
        token = item.jwt;
        localStorage.setItem("token", item.access_token);
        checkPermission(item.access_token);
      }
    } else if (!username && !password) {
      userName_alert = "red";
      password_alert = "red";
      setInterval(function () {
        userName_alert = "black";
        password_alert = "black";
      }, 3000);
    } else if (!username || password) {
      userName_alert = "red";
      setInterval(function () {
        userName_alert = "black";
      }, 3000);
    } else if (username || !password) {
      password_alert = "red";
      setInterval(function () {
        password_alert = "black";
      }, 3000);
    }
  }

  function checkPermission(event) {
    if (!event) {
      window.location.href = "/login";
      return;
    } else {
      window.location.href = `/profile?username=${username}`;
    }
  }
</script>

<Navbar {username} />

<br /><br />

<div class="text-center">
  <main class="form-signin w-100 m-auto">
    <form>
      <img
        class="mb-4"
        src="https://getbootstrap.com/docs/5.3/assets/brand/bootstrap-logo.svg"
        alt=""
        width="72"
        height="57"
      />
      <h1 class="h3 mb-3 fw-normal">Please sign in</h1>

      <div style:color={userName_alert} class="form-floating">
        <input
          type="username"
          class="form-control"
          id="floatingInput"
          bind:value={username}
          placeholder="example"
        />
        <label for="floatingInput">User name</label>
      </div>
      <div style:color={password_alert} class="form-floating">
        <input
          type="password"
          class="form-control"
          id="floatingPassword"
          bind:value={password}
          placeholder="Password"
        />
        <label for="floatingPassword">Password</label>
      </div>

      <div class="checkbox mb-3">
        <label>
          <input
            type="checkbox"
            value="remember-me"
            on:click={checkbox}
            bind:checked={remember_me}
          /> Remember me
        </label>
      </div>
      <button
        class="w-100 btn btn-lg btn-primary"
        on:click={doPostLogin}
        on:dblclick={handleClick}
        type="submit">Sign in</button
      >
      <p class="mt-5 mb-3 text-muted">© 2017-2022</p>
    </form>
  </main>
</div>
<Footer />

<style>
  /* html,
  body {
    height: 100%;
  }
  body {
    display: flex;
    align-items: center;
    padding-top: 40px;
    padding-bottom: 40px;
    background-color: #f5f5f5;
  } */

  .form-signin {
    max-width: 330px;
    padding: 15px;
  }
  .form-signin .form-floating:focus-within {
    z-index: 2;
  }
  /* .form-signin input[type="email"] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  } */
  .form-signin input[type="password"] {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }
</style>
