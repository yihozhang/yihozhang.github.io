new Vue({
    el:"#main",
    mounted: function() {
        axios.get('/blog/posts/manifest.json').then((response)=>{
            this.posts=response.data.sort((a,b)=>a.id<b.id);
        });
    },
    data: {
        posts:[],
    },
})