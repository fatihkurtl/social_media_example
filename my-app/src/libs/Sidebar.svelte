<script>
  import "bootstrap/dist/css/bootstrap.min.css";
</script>

<div
  class="d-flex flex-column flex-shrink-0 p-3 text-bg-dark"
  style="width: 280px; height: 647px; overflow: auto;"
  id="sideBar"
>
  <a
    href="/"
    class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none"
  >
    <svg class="bi pe-none me-2" width="40" height="32"
      ><use xlink:href="#bootstrap" /></svg
    >
    <span class="fs-4">Sidebar</span>
  </a>
  <hr />
  <ul class="nav nav-pills flex-column mb-auto">
    <li class="nav-item">
      <a href="/home" class="nav-link active" aria-current="page">
        <svg class="bi pe-none me-2" width="16" height="16"
          ><use xlink:href="#home" /></svg
        >
        Home
      </a>
    </li>
    <li>
      <a href="/friends" class="nav-link text-white">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-people me-2"
          viewBox="0 0 16 16"
        >
          <path
            d="M15 14s1 0 1-1-1-4-5-4-5 3-5 4 1 1 1 1h8Zm-7.978-1A.261.261 0 0 1 7 12.996c.001-.264.167-1.03.76-1.72C8.312 10.629 9.282 10 11 10c1.717 0 2.687.63 3.24 1.276.593.69.758 1.457.76 1.72l-.008.002a.274.274 0 0 1-.014.002H7.022ZM11 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm3-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM6.936 9.28a5.88 5.88 0 0 0-1.23-.247A7.35 7.35 0 0 0 5 9c-4 0-5 3-5 4 0 .667.333 1 1 1h4.216A2.238 2.238 0 0 1 5 13c0-1.01.377-2.042 1.09-2.904.243-.294.526-.569.846-.816ZM4.92 10A5.493 5.493 0 0 0 4 13H1c0-.26.164-1.03.76-1.724.545-.636 1.492-1.256 3.16-1.275ZM1.5 5.5a3 3 0 1 1 6 0 3 3 0 0 1-6 0Zm3-2a2 2 0 1 0 0 4 2 2 0 0 0 0-4Z"
          />
        </svg>
        Friends
      </a>
    </li>
    <li>
      <a href="/share" class="nav-link text-white">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-share me-2"
          viewBox="0 0 16 16"
        >
          <path
            d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.499 2.499 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5zm-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"
          />
        </svg>
        Share
      </a>
    </li>
    <li>
      <a href="/discovery" class="nav-link text-white">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-globe-europe-africa me-2"
          viewBox="0 0 16 16"
        >
          <path
            d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0ZM3.668 2.501l-.288.646a.847.847 0 0 0 1.479.815l.245-.368a.809.809 0 0 1 1.034-.275.809.809 0 0 0 .724 0l.261-.13a1 1 0 0 1 .775-.05l.984.34c.078.028.16.044.243.054.784.093.855.377.694.801-.155.41-.616.617-1.035.487l-.01-.003C8.274 4.663 7.748 4.5 6 4.5 4.8 4.5 3.5 5.62 3.5 7c0 1.96.826 2.166 1.696 2.382.46.115.935.233 1.304.618.449.467.393 1.181.339 1.877C6.755 12.96 6.674 14 8.5 14c1.75 0 3-3.5 3-4.5 0-.262.208-.468.444-.7.396-.392.87-.86.556-1.8-.097-.291-.396-.568-.641-.756-.174-.133-.207-.396-.052-.551a.333.333 0 0 1 .42-.042l1.085.724c.11.072.255.058.348-.035.15-.15.415-.083.489.117.16.43.445 1.05.849 1.357L15 8A7 7 0 1 1 3.668 2.501Z"
          />
        </svg>
        Discovery
      </a>
    </li>
    <li>
      <a href="/profile" class="nav-link text-white">
        <svg class="bi pe-none me-2" width="16" height="16"
          ><use xlink:href="#people-circle" /></svg
        >
        Profile
      </a>
    </li>
  </ul>
  <hr />
  <div class="dropdown">
    <a
      href="/"
      class="d-flex align-items-center text-white text-decoration-none dropdown-toggle"
      data-bs-toggle="dropdown"
      aria-expanded="false"
    >
      <img
        src="https://github.com/mdo.png"
        alt=""
        class="rounded-circle me-2"
        width="32"
        height="32"
      />
      <strong>mdo</strong>
    </a>
    <ul class="dropdown-menu dropdown-menu-dark text-small shadow">
      <li><a class="dropdown-item" href="/">New project...</a></li>
      <li><a class="dropdown-item" href="/">Settings</a></li>
      <li><a class="dropdown-item" href="/">Profile</a></li>
      <li><hr class="dropdown-divider" /></li>
      <li><a class="dropdown-item" href="/">Sign out</a></li>
    </ul>
  </div>
</div>

<style>
</style>
