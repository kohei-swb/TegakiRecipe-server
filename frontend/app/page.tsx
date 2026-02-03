import Message from './Message';
import ClientButton from '../components/AddRecipe'
import Recipe from '@/components/Recipe';
function Page(){
  return (
  <>
    <div className="grid h-56 grid-cols-2 content-start gap-4 ...">
      <h1 className='text-4xl px-4 py-2'>レシピ</h1>
      <ClientButton />
    </div>
    <Recipe/>
    
  </>
 );
 
}

export default Page;