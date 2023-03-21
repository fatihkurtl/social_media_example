<script>
  import Footer from "../../libs/Footer.svelte";
  import "bootstrap/dist/css/bootstrap.min.css";
  import Navbar from "../../libs/Navbar.svelte";

  let firstName;
  let lastName;
  let userName;
  let email;
  // let file;
  let url;
  let password;
  let password2;
  let checkBox = false;
  let checkColor;

  const checkedBox = () => {
    checkBox == true ? (checkBox = false) : (checkBox = true);
    if (checkBox == true) {
      checkColor = 'green';
    }
    else {
      checkColor = '';
    }
  };

  async function doPost() {
    if (checkBox == true) {
      const res = await fetch("http://127.0.0.1:5173/user/register", {
        method: "POST",
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          user_name: userName,
          e_mail: email,
          // user_file: file,
          user_profile_photo: url,
          user_password: password,
          user_password2: password2,
        }),
      });
      const item = await res.json();
      if (item.status == 200 && item.info == true) {
        window.location.href = "/login";
      }
    }
  }
</script>

<Navbar />
<br />

<div class="container p-5 mb-4 bg-light rounded-3">
  <div class="bd-example-snippet bd-code-snippet">
    <div class="bd-example">
      <form class="row g-3">
        <div class="col-md-4">
          <label for="validationServer01" class="form-label">First name</label>
          <input
            type="text"
            class="form-control is-valid"
            id="validationServer01"
            bind:value={firstName}
            required=""
          />
          {#if firstName}
            <div class="valid-feedback">Looks good!</div>
          {/if}
        </div>
        <div class="col-md-4">
          <label for="validationServer02" class="form-label">Last name</label>
          <input
            type="text"
            class="form-control is-valid"
            id="validationServer02"
            bind:value={lastName}
            required=""
          />
          {#if lastName}
            <div class="valid-feedback">Looks good!</div>
          {/if}
        </div>
        <div class="col-md-4">
          <label for="validationServerUsername" class="form-label"
            >Username</label
          >
          <div class="input-group has-validation">
            <span class="input-group-text" id="inputGroupPrepend3">@</span>
            <input
              type="text"
              class="form-control is-valid"
              id="validationServerUsername"
              aria-describedby="inputGroupPrepend3"
              bind:value={userName}
              required=""
            />
            {#if userName}
              <div class="invalid-feedback">Please choose a username.</div>
            {/if}
          </div>
        </div>
        <div class="col-md-6">
          <label for="validationServer01" class="form-label">E-mail</label>
          <input
            type="text"
            class="form-control is-valid"
            id="validationServer01"
            bind:value={email}
            required=""
          />
          {#if email}
            <div class="valid-feedback">Looks good!</div>
          {/if}
        </div>
        <div class="col-md-6">
          <!-- <label for="formFileLg" class="form-label">Profile Photo</label>
          <input
            class="form-control is-valid"
            id="validationServerUsername"
            aria-describedby="inputGroupPrepend3"
            required=""
            bind:value={file}
            type="file"
          /> -->
          <label for="formFileLg" class="form-label">Profile Photo</label>
          <input
            class="form-control is-valid"
            id="validationServerUsername"
            aria-describedby="inputGroupPrepend3"
            required=""
            bind:value={url}
            type="url"
            placeholder="profile_photojpg.com"
          />
        </div>
        <div class="col-md-4">
          <label for="validationServer03" class="form-label">Password</label>
          <input
            type="password"
            class="form-control is-valid"
            id="validationServer02"
            bind:value={password}
            required=""
          />
          <div class="invalid-feedback">Please enter a password.</div>
        </div>
        <div class="col-md-4">
          <label for="validationServer03" class="form-label"
            >*Password Again</label
          >
          <input
            type="password"
            class="form-control is-valid"
            id="validationServer02"
            bind:value={password2}
            required=""
          />
          <div class="invalid-feedback">Please enter a password.</div>
        </div>
        <div class="col-12">
          <div class="form-check">
            <input
              class="form-check-input is-invalid"
              type="checkbox"
              value=""
              id="invalidCheck3"
              on:click={checkedBox}
              bind:checked={checkBox}
              required=""
            />
            <label class="form-check-label" for="invalidCheck3" style:color={checkColor}>
              Agree to terms and conditions
            </label>
            <div class="invalid-feedback" style:color={checkColor}>
              You must agree before submitting.
            </div>
          </div>
        </div>
        <div class="col-12">
          <button class="btn btn-primary" type="submit" on:click={doPost}
            >Submit form</button
          >
        </div>
      </form>
    </div>
  </div>
</div>

<Footer />
