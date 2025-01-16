import {createClient} from '@supabase/supabase-js'
import * as dotenv from 'dotenv'; dotenv.config();
import {readFile} from "fs/promises";
import iter_posts from "./extractor.js";



const supabaseUrl = process.env.SUPABASE_URL
const supabaseKey = process.env.SUPABASE_KEY
const supabaseClient = createClient(supabaseUrl, supabaseKey)
export default supabaseClient

if (import.meta.url === `file://${process.argv[1]}`) {

    // const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    // const t2 = timestamp.slice(0,10)
    // console.log(t2)
    // const {data, error} = await supabaseClient.from('sources').update({'last_scraped':t2}).match({'id':61})
    // console.log(error)


    // const {data, error } = await supabaseClient
        //     .from('posts')
        //     .select('id, url_slug')
        //     .eq('url_slug', 'DEkCUwqtM2q')
        // console.log(data.length)

    // {
    //     const {data, error } = await supabaseClient
    //         .from('sources')
    //         .select('slug')
    //         .eq('media', 'insta')
    //         .eq('category', 'dance')
    //         .eq('city', 'Київ')
    //     console.log(data)
    // }

    // {
    //     const {data, error} = await supabaseClient
    //         .from('test')
    //         .insert([
    //             {text: 'value18'},
    //         ])
    // }

    // {
    //     const {data, error} = await supabaseClient
    //         .from('test')
    //         .select()
    //
    //     console.log(data)
    // }
}

