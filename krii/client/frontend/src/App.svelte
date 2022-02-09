<script>
    import axios from "axios"

    let name = "Vinny";
    let age = 1;

    function increment() {
        age += 1;

        axios.get("http://localhost:3000/blocks")
            .then(function(response) {
                console.log(response);
            })
    }
</script>

<h1>Hello {name}, you're {age} today!</h1>
<button on:click={increment} class="btn btn-primary">Add</button>