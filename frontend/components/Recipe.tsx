'use client'
function Recipe(){
    return(
    <div className="flex items-center space-x-4 rtl:space-x-reverse">
         <div className="flex-1 min-w-0 px-5">
            <p className="text-2xl font-medium text-heading truncate">
               Recipe name
            </p>
            <p className="text-1xl text-body truncate">
               ingredients
            </p>
         </div>
      </div>
    )
}

export default Recipe;