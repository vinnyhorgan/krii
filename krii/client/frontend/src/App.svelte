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