<script lang="ts">
	let { recipe } = $props();

	function parseIngredients(ingredientsStr: string) {
		try {
			return JSON.parse(ingredientsStr);
		} catch {
			return {};
		}
	}

	function getIngredientCount(ingredientsStr: string) {
		const ingredients = parseIngredients(ingredientsStr);
		return Object.keys(ingredients).length;
	}
</script>

<a
	href="/recipes/{recipe.id}"
	class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow duration-300"
>
	<div class="card-body">
		<h2 class="card-title text-xl">
			{recipe.name}
			<div class="badge badge-primary">{recipe.category_name}</div>
		</h2>

		<p class="text-sm text-base-content/70 line-clamp-2">
			{recipe.description}
		</p>

		<div class="divider my-2"></div>

		<div class="flex flex-wrap gap-3 text-sm">
			<div class="flex items-center gap-1">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-4 w-4"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
					/>
				</svg>
				<span>{recipe.prep_time} min</span>
			</div>

			<div class="flex items-center gap-1">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-4 w-4"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
					/>
				</svg>
				<span>{recipe.servings} servings</span>
			</div>

			<div class="flex items-center gap-1">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-4 w-4"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
					/>
				</svg>
				<span>{getIngredientCount(recipe.ingredients)} ingredients</span>
			</div>

			<div class="flex items-center gap-1">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-4 w-4"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M13 10V3L4 14h7v7l9-11h-7z"
					/>
				</svg>
				<span>{recipe.calories} cal</span>
			</div>
		</div>

		<div class="card-actions justify-end mt-4">
			<button class="btn btn-primary btn-sm">View Recipe</button>
		</div>
	</div>
</a>
