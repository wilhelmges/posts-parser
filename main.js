const {createClient} = supabase



document.addEventListener('alpine:init', () => {
    const supabase = createClient('https://myfvudumhgbrufiiclxn.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im15ZnZ1ZHVtaGdicnVmaWljbHhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUwNTg0NDcsImV4cCI6MjA1MDYzNDQ0N30.C1p1G5lDsOhjSMWWKIX58Ct4QQVRUhTX_KyFDZ9qJOw')
    Alpine.data('posts', () => ({
        greeting: 'dynamic',
        items: [],
        posts: [],
        initData: async function (url = 'http://localhost:1337/api/raw-posts') {
            console.log('hello, posts');
            try {
                const {data, error3} = await supabase.from('posts').select('id, fulltext, source_slug,created_at').eq('status', 'notreviewed')
                    .eq('category','dance').limit(25).order('created_at', { ascending: false });
                console.log(data);
                this.posts = data;
            } catch (error) {
                console.error('Error:', error.message);
            }
        },
        arxivPost: async function (id){
            console.log(id);
            const {error} = await supabase.from('posts').update({status: 'arxived'}).eq('id', id)
            let indexToRemove = this.posts.findIndex(item => item.id === id);
            if (indexToRemove !== -1) {
                this.posts.splice(indexToRemove, 1);
            }
        },
        repostPost: async function (id){
            console.log(id);
            const {error} = await supabase.from('posts').update({status: 'torepost'}).eq('id', id)
            let indexToRemove = this.posts.findIndex(item => item.id === id);
            if (indexToRemove !== -1) {
                this.posts.splice(indexToRemove, 1);
            }
        }
    }))
})

async function processdata() {
//    const supabase = createClient('https://wepnusszkcvcxrtnwpbe.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlcG51c3N6a2N2Y3hydG53cGJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDY4ODcwNzQsImV4cCI6MjAyMjQ2MzA3NH0.6vYE9OyGZ0yGwgeFpL6U3sS5eJVPhyEn1tE_owSdynI')

    const {error1} = await supabase
        .from('categories')
        .insert({title: 'skating'})

    const {error2} = await supabase
        .from('categories')
        .delete()
        .eq('id', 3)

    const {data, error3} = await supabase
        .from('categories')
        .select()
    console.log(data);
}
