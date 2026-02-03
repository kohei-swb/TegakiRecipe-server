'use client'

interface Recipe {
    recipe_name: string;
    ingredients: string[];
}

function AddRecipe(){
    // const addRecipe = () => console.log('clicked');
    function addRecipe(){
        console.log('clicked');
    }
    return (<button className='bg-blue-500 text-white font-bold py-2 px-4 rounded' onClick={addRecipe}>レシピを追加</button>)
}

export default AddRecipe;