import {createClient} from '@supabase/supabase-js'
import * as dotenv from 'dotenv';
import {readFile} from "fs/promises";
import iter_posts from "./extractor.js";

dotenv.config();

const supabaseUrl = process.env.SUPABASE_URL
const supabaseKey = process.env.SUPABASE_KEY
const supabaseClient = createClient(supabaseUrl, supabaseKey)

if (import.meta.url === `file://${process.argv[1]}`) {
    {
        const {data, error} = await supabaseClient
            .from('test')
            .insert([
                {text: 'value18'},
            ])
    }

    {
        const {data, error} = await supabaseClient
            .from('test')
            .select()

        console.log(data)
    }
}

