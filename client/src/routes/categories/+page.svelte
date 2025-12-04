<script lang="ts">
	import type { PageProps } from './$types';
	import { env } from '$env/dynamic/public';

	import { currentUser } from '$lib/stores/state.svelte';
	import { invalidateAll } from '$app/navigation';

	let { data }: PageProps = $props();
	let showCreateModal = $state(false);
	let errors: string[] = $state([]);
	let name = $state('');
	let description = $state('');
	let parent_category = $state(0);

	let showEditCategoryModal = $state(false);
	let edit_category_id = $state<number | null>(null);
	let edit_category_name = $state('');
	let edit_category_description = $state('');
	let edit_category_parent = $state('');

	// Function to open comment edit modal
	const openEditCategoryModal = (category: any) => {
		edit_category_id = category.id;
		edit_category_name = category.name;
		edit_category_description = category.description;
		edit_category_parent = category.parent_category;
		showEditCategoryModal = true;
	};

	const handleCategoryDelete = async (event: Event, categoryId: number) => {
		event.preventDefault();
		errors = [];

		try {
			const response = await fetch(`${env.PUBLIC_API_URL}/categories/${categoryId}`, {
				method: 'DELETE',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include'
			});

			if (!response.ok) {
				const data = await response.json();

				if (response.status === 422 && data.detail) {
					// Handle validation errors
					errors = data.detail.map((err: any) => err.msg);
				} else if (data.message) {
					// Handle general error message
					errors = [data.message];
				} else {
					errors = ['An unexpected error occurred'];
				}
			} else {
				data.categories = data.categories.filter((c) => c.id !== categoryId);
				invalidateAll();
			}
		} catch (error) {
			errors = ['Network error. Please try again.'];
		}
	};

	const handleCategoryUpdate = async (event: Event) => {
		event.preventDefault();
		errors = [];

		try {
			const response = await fetch(`${env.PUBLIC_API_URL}/categories/${edit_category_id}`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify({
					name: edit_category_name,
					description: edit_category_description,
					parent_category: edit_category_parent
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
				showEditCategoryModal = false;
				invalidateAll();
			}
		} catch (error) {
			errors = ['Network error. Please try again.'];
		}
	};

	const handleCategoryCreate = async (event: Event) => {
		event.preventDefault();
		errors = [];

		try {
			const response = await fetch(`${env.PUBLIC_API_URL}/categories/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify({
					name,
					description,
					parent_category
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

<div class="min-h-screen mt-8">
	<div class="container mx-auto px-4 py-12">
		<div class="text-center mb-12">
			<h1 class="text-5xl font-bold text-base-content mb-4">Recipe Categories</h1>
			<p class="text-lg text-base-content/70">Explore our collection of delicious recipes</p>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each data.categories.filter((c: any) => c.parent_category !== null) as category (category.id)}
				<div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow duration-300">
					<div class="card-body">
						<h2 class="card-title text-2xl">{category.name}</h2>
						<p class="text-base-content/70">{category.description}</p>
						<div class="card-actions justify-end mt-4">
							<a href="/categories/{category.id}/recipes" class="btn btn-primary">View Recipes</a>
						</div>
					</div>
					{#if currentUser.logged_in && currentUser.role === 'ADMIN'}
						<div class="card-actions justify-end mt-4 pt-4 border-t pr-[1.5rem] pb-[1rem]">
							<button
								onclick={() => openEditCategoryModal(category)}
								class="btn btn-primary btn-sm"
							>
								Edit
							</button>
							<button
								onclick={(e) => handleCategoryDelete(e, category.id)}
								class="btn btn-error btn-sm"
							>
								Delete
							</button>
						</div>
					{/if}
				</div>
			{/each}

			{#if currentUser.logged_in && currentUser.role === 'ADMIN'}
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

					Create category
				</button>
			{/if}
		</div>
	</div>
</div>

{#if showCreateModal}
	<dialog class="modal modal-open">
		<div class="modal-box">
			<h3 class="font-bold text-lg mb-4">Edit Comment</h3>
			<form onsubmit={handleCategoryCreate}>
				<div class="form-control mb-3">
					<label class="label" for="category-title">
						<span class="label-text">Title</span>
					</label>
					<input
						bind:value={name}
						type="text"
						id="category-title"
						placeholder="Give your category a name"
						class="input input-bordered w-full"
						required
					/>
				</div>

				<div class="form-control mb-3">
					<label class="label" for="category-parent">
						<span class="label-text">Parent category id</span>
					</label>
					<input
						bind:value={parent_category}
						type="number"
						id="category-parent"
						placeholder="Enter id of parent category"
						class="input input-bordered w-full"
						required
					/>
				</div>

				<div class="form-control mb-4">
					<label class="label" for="category-description">
						<span class="label-text">Description</span>
					</label>
					<textarea
						id="category-decription"
						bind:value={description}
						class="textarea textarea-bordered h-24 w-full"
						placeholder="Enter category description..."
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

{#if showEditCategoryModal}
	<dialog class="modal modal-open">
		<div class="modal-box">
			<h3 class="font-bold text-lg mb-4">Edit Category</h3>
			<form onsubmit={handleCategoryUpdate}>
				<div class="form-control mb-3">
					<label class="label" for="category-title">
						<span class="label-text">Name</span>
					</label>
					<input
						bind:value={edit_category_name}
						type="text"
						id="category-title"
						placeholder="Give your category a name"
						class="input input-bordered w-full"
						required
					/>
				</div>

				<div class="form-control mb-3">
					<label class="label" for="category-parent">
						<span class="label-text">Parent category id</span>
					</label>
					<input
						bind:value={edit_category_parent}
						type="number"
						id="category-parent"
						placeholder="Enter id of parent category"
						class="input input-bordered w-full"
						required
					/>
				</div>

				<div class="form-control mb-4">
					<label class="label" for="category-description">
						<span class="label-text">Description</span>
					</label>
					<textarea
						id="category-decription"
						bind:value={edit_category_description}
						class="textarea textarea-bordered h-24 w-full"
						placeholder="Enter category description..."
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
					<button type="button" class="btn" onclick={() => (showEditCategoryModal = false)}
						>Cancel</button
					>
					<button type="submit" class="btn btn-primary">Submit</button>
				</div>
			</form>
		</div>
		<form method="dialog" class="modal-backdrop">
			<button onclick={() => (showEditCategoryModal = false)}>close</button>
		</form>
	</dialog>
{/if}
