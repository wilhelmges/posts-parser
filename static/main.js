const {createClient} = supabase

const PostStatus = {
    ALL: 'all',
    NOT_REVIEWED: 'notreviewed',
    NEED_SUMMARY: 'needsummary',
    READYTOPOST: 'readytopost',
    ARCHIVED: 'archived'
};

document.addEventListener('alpine:init', () => {
    const supabase = createClient('https://myfvudumhgbrufiiclxn.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im15ZnZ1ZHVtaGdicnVmaWljbHhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUwNTg0NDcsImV4cCI6MjA1MDYzNDQ0N30.C1p1G5lDsOhjSMWWKIX58Ct4QQVRUhTX_KyFDZ9qJOw')
    
    Alpine.data('posts', () => ({
        locale: 'uk',
        currentFilter: PostStatus.NOT_REVIEWED,
        posts: [],
        
        initData: async function () {
            try {
                const {data, error} = await supabase
                    .from('posts')
                    .select('id, fulltext, brief, source_slug, event_date')
                    .eq('status', this.currentFilter)
                    .eq('category', 'dance')
                    .limit(25)
                    .order('created_at', { ascending: false });
                
                if (error) throw error;
                this.posts = data;
            } catch (error) {
                console.error('Error:', error.message);
            }
        },

        updatePost: async function(id, value) {
            try {
                const {error} = await supabase
                    .from('posts')
                    .update({fulltext: value})
                    .eq('id', id);
                    
                if (error) throw error;
                
                const post = this.posts.find(p => p.id === id);
                if (post) {
                    post.fulltext = value;
                }
            } catch (error) {
                console.error('Error updating post:', error.message);
            }
        },

        formatDate: function(dateString) {
            return new Date(dateString).toLocaleString('uk-UA');
        },

        markPostAsArchived: async function (id) {
            try {
                const {error} = await supabase
                    .from('posts')
                    .update({status: PostStatus.ARCHIVED})
                    .eq('id', id);
                
                if (error) throw error;
                this.posts = this.posts.filter(post => post.id !== id);
            } catch (error) {
                console.error('Error:', error.message);
            }
        },

        markAsNeedSummary: async function(id) {
            try {
                const {error} = await supabase
                    .from('posts')
                    .update({status: PostStatus.NEED_SUMMARY})
                    .eq('id', id);
                
                if (error) throw error;
                
                this.posts = this.posts.filter(post => post.id !== id);
            } catch (error) {
                console.error('Помилка при оновленні статусу:', error.message);
            }
        },


        markAsReady: async function(id) {
            try {
                const {error} = await supabase
                    .from('posts')
                    .update({status: PostStatus.READYTOPOST})
                    .eq('id', id);
                
                if (error) throw error;
                
                // Видаляємо пост з поточного списку відображення
                this.posts = this.posts.filter(post => post.id !== id);
            } catch (error) {
                console.error('Помилка при позначенні поста як готового:', error.message);
            }
        },

        restoreFromArchive: async function(id) {
            try {
                const {error} = await supabase
                    .from('posts')
                    .update({status: PostStatus.NOT_REVIEWED})
                    .eq('id', id);
                    
                if (error) throw error;
                
                // Видаляємо пост з поточного списку відображення
                this.posts = this.posts.filter(post => post.id !== id);
            } catch (error) {
                console.error('Помилка при відновленні поста з архіву:', error.message);
            }
        },

        updateBrief: async function(id, value) {
            try {
                const {error} = await supabase
                    .from('posts')
                    .update({brief: value})
                    .eq('id', id);
                    
                if (error) throw error;
                
                const post = this.posts.find(p => p.id === id);
                if (post) {
                    post.brief = value;
                }
            } catch (error) {
                console.error('Помилка оновлення короткого опису:', error.message);
            }
        },

        updateEventDate: async function(id, value) {
            try {
                const {error} = await supabase
                    .from('posts')
                    .update({event_date: value})
                    .eq('id', id);
                    
                if (error) throw error;
                
                const post = this.posts.find(p => p.id === id);
                if (post) {
                    post.event_date = value;
                }
            } catch (error) {
                console.error('Помилка оновлення дати події:', error.message);
            }
        },

        parseSources: async function() {
            try {
                const response = await fetch('/api/scan');
                const data = await response.json();
                
                if (data.status === 'success') {
                    console.log('Джерела проскановано:', data.message);
                    await this.initData(); // Оновлюємо дані після сканування
                } else {
                    throw new Error(data.message || 'Помилка при скануванні джерел');
                }
            } catch (error) {
                console.error('Помилка:', error.message);
            }
        },

        getSummaries: async function() {
            try {
                const response = await fetch('/api/getsummaries');
                const data = await response.json();
                
                if (data.status === 'success') {
                    console.log('Оброблено постів:', data.processed);
                    await this.initData(); // Оновлюємо дані після обробки
                } else {
                    throw new Error('Помилка при обробці постів');
                }
            } catch (error) {
                console.error('Помилка:', error.message);
            }
        },

        publishDigests: async function() {
            try {
                const response = await fetch('/api/publishdigests');
                const data = await response.json();
            } catch (error) {
                console.error('Помилка:', error.message);
            }
        },

        updateUrlAndData() {
            const url = new URL(window.location);
            url.searchParams.set('status', this.currentFilter);
            window.history.pushState({}, '', url);
            this.initData();
        },

        initDataFromUrl() {
            const params = new URLSearchParams(window.location.search);
            const status = params.get('status');
            if (status) {
                this.currentFilter = status;
            }
            this.initData();
        },

        init() {
            this.initDataFromUrl();
            this.$watch('currentFilter', () => {
                this.initData();
            });
        }
    }))
})
