<script>
    let blocks = []

    let blockExplorer = true
    let nodes = false

    function pageBlockExplorer() {
        blockExplorer = true
        nodes = false
    }

    function pageNodes() {
        blockExplorer = false
        nodes = true
    }

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

    setInterval(function(){
        getBlocks();
    }, 1000);
</script>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
        <a href="/" class="navbar-brand">Admin</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbar">
            <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a on:click={pageBlockExplorer} href="#" class="nav-link">Block Explorer</a>
                </li>
                <li class="nav-item">
                    <a on:click={pageNodes} href="#" class="nav-link">Nodes</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

{#if blockExplorer == true}
    <div class="container">
        {#each blocks as block}
            <div class="card m-4">
                <div class="card-body">
                    <h4 class="card-title">
                        Block: {block["index"]}
                    </h4>
                    <p class="card-text">
                        Previous Hash: {block["previous_hash"]}
                    </p>
                    <p class="card-text">
                        Timestamp: {block["timestamp"]}
                    </p>
                    <p class="card-text">
                        Nonce: {block["nonce"]}
                    </p>
                    <p class="card-text">
                        Hash: {block["hash"]}
                    </p>
                </div>
            </div>
        {/each}
    </div>
{:else if nodes == true}
    <h1>Nodes</h1>
{/if}