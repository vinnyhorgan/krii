<script>
    let blocks = []

    function getBlocks() {
        let request = new XMLHttpRequest();
        request.open("GET", "http://localhost:5000/blocks");
        request.send();
        request.onload = () => {
            if (request.status === 200) {
                blocks = JSON.parse(request.response)["blocks"];
                console.log(blocks);
            } else {
                console.log("Error");
            }
        }
    }

    getBlocks();
</script>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
        <a href="/" class="navbar-brand">Admin</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbar">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a href="/" class="nav-link">Blockchain</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<button on:click={getBlocks} class="btn btn-primary">Fetch</button>

<div class="container">
    {#each blocks as block}
        <div class="card">
            <div class="card-body">
                <h4 class="card-title">
                    Block: {block["index"]}
                </h4>
                <p class="card-text">
                    Previous Hash: {block["previous_hash"]}
                </p>
                <p class="card-text">
                    Proof: {block["proof"]}
                </p>
                <p class="card-text">
                    Timestamp: {block["timestamp"]}
                </p>
            </div>
        </div>
    {/each}
</div>