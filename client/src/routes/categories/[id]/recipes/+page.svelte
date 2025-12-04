<script lang="ts">
	import type { PageProps } from './$types';
	import Recipe from '$lib/Recipe.svelte';
	let { data }: PageProps = $props();

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

<div class="container mx-auto px-4 py-8">
	<h1 class="text-4xl font-bold mb-8 text-center">Recipe Collection</h1>

	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 md:gap-10 gap-6">
		{#each data.recipes as recipe}
			<Recipe {recipe} />
		{/each}
	</div>
</div>

<style>
	.line-clamp-2 {
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>
