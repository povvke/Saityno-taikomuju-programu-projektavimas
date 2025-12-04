<script lang="ts">
	import { currentUser } from '$lib/stores/state.svelte';
	import { env } from '$env/dynamic/public';
	import type { PageProps } from './$types';
	import Recipe from '$lib/Recipe.svelte';
	import { invalidateAll } from '$app/navigation';
	let { data }: PageProps = $props();

	let showCreateModal = $state(false);
	let errors: string[] = $state([]);

	let name = $state('');
	let description = $state('');
	let prep_time = $state(0);
	let servings = $state(0);
	let calories = $state(0);
	let instructions = $state('');
	let ingredients = $state('');

	const handleRecipeCreate = async (event: Event) => {
		event.preventDefault();
		errors = [];

		try {
			const response = await fetch(`${env.PUBLIC_API_URL}/recipes/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify({
					name,
					description,
					prep_time,
					servings,
					calories,
					instructions,
					ingredients,
					category_id: data.category_id
				})
			});

			if (!response.ok) {
				const data = await response.json();
				if (response.status === 422 && data.detail) {
					errors = data.detail.map((err: any) => err.msg);
				} else if (data.message) {
					errors = [data.message];
				} else {
					errors = ['An unexpected error occurred'];
				}
			} else {
				showCreateModal = false;
				invalidateAll();
			}
		} catch (error) {
			errors = ['Network error. Please try again.'];
		}
	};
</script>

<div class="container mx-auto px-4 py-8">
	<h1 class="text-4xl font-bold mb-8 text-center">Recipe Collection</h1>

	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 md:gap-10 gap-6">
		{#each data.recipes as recipe}
			<Recipe {recipe} />
		{/each}

		{#if currentUser.logged_in}
			<button
				class="btn btn-secondary btn-sm w-fit"
				onclick={() => {
					showCreateModal = true;
				}}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="size-6"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
					/>
				</svg>

				Create recipe
			</button>
		{/if}
	</div>
</div>

{#if showCreateModal}
	<dialog class="modal modal-open">
		<div class="modal-box max-w-2xl">
			<h3 class="font-bold text-lg mb-4">Edit Recipe</h3>
			<form onsubmit={handleRecipeCreate}>
				<div class="form-control mb-3">
					<label class="label" for="edit-name">
						<span class="label-text">Recipe Name</span>
					</label>
					<input
						bind:value={name}
						type="text"
						id="edit-name"
						class="input input-bordered w-full"
						required
					/>
				</div>

				<div class="form-control mb-3">
					<label class="label" for="edit-description">
						<span class="label-text">Description</span>
					</label>
					<textarea
						bind:value={description}
						id="edit-description"
						class="textarea textarea-bordered h-20 w-full"
						required
					></textarea>
				</div>

				<div class="grid grid-cols-3 gap-3 mb-3">
					<div class="form-control">
						<label class="label" for="edit-prep-time">
							<span class="label-text">Prep Time (min)</span>
						</label>
						<input
							bind:value={prep_time}
							type="number"
							id="edit-prep-time"
							class="input input-bordered"
							required
						/>
					</div>

					<div class="form-control">
						<label class="label" for="edit-servings">
							<span class="label-text">Servings</span>
						</label>
						<input
							bind:value={servings}
							type="number"
							id="edit-servings"
							class="input input-bordered"
							required
						/>
					</div>

					<div class="form-control">
						<label class="label" for="edit-calories">
							<span class="label-text">Calories</span>
						</label>
						<input
							bind:value={calories}
							type="number"
							id="edit-calories"
							class="input input-bordered"
							required
						/>
					</div>
				</div>

				<div class="form-control mb-3">
					<label class="label" for="edit-ingredients">
						<span class="label-text">Ingredients (JSON format)</span>
					</label>
					<textarea
						bind:value={ingredients}
						id="edit-ingredients"
						class="textarea textarea-bordered h-24 font-mono text-sm w-full"
						required
					></textarea>
				</div>

				<div class="form-control mb-4">
					<label class="label" for="edit-instructions">
						<span class="label-text">Instructions</span>
					</label>
					<textarea
						bind:value={instructions}
						id="edit-instructions"
						class="textarea textarea-bordered h-32 w-full"
						required
					></textarea>
				</div>

				{#if errors.length > 0}
					<div class="alert alert-error mb-4">
						{#each errors as error}
							<p>{error}</p>
						{/each}
					</div>
				{/if}

				<div class="modal-action">
					<button type="button" class="btn" onclick={() => (showCreateModal = false)}>Cancel</button
					>
					<button type="submit" class="btn btn-primary">Submit</button>
				</div>
			</form>
		</div>
		<form method="dialog" class="modal-backdrop">
			<button onclick={() => (showCreateModal = false)}>close</button>
		</form>
	</dialog>
{/if}

<style>
	.line-clamp-2 {
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>
