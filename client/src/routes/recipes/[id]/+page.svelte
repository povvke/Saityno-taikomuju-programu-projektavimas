<script lang="ts">
	import type { PageProps } from './$types';
	import { env } from '$env/dynamic/public';
	import { currentUser } from '$lib/stores/state.svelte';
	import { invalidateAll } from '$app/navigation';

	let { data }: PageProps = $props();
	let errors = [];
	let comment_title = $state('');
	let comment_text = $state('');
	let comment_rating = $state(5);
	let recipe_id = data.recipe.id;

	const ingredients = JSON.parse(data.recipe.ingredients);

	const handleCommentDelete = async (event: Event, commentId: number) => {
		event.preventDefault();
		errors = [];

		try {
			const response = await fetch(`${env.PUBLIC_API_URL}/comments/${commentId}`, {
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
				data.comments = data.comments.filter((c) => c.id !== commentId);
				invalidateAll();
			}
		} catch (error) {
			errors = ['Network error. Please try again.'];
		}
	};

	const handleComment = async (event: Event) => {
		event.preventDefault();
		errors = [];

		try {
			const response = await fetch(`${env.PUBLIC_API_URL}/comments/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify({
					title: comment_title,
					text: comment_text,
					rating: comment_rating,
					recipe_id
				})
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
				const res_data = await response.json();
				data.comments = [...data.comments, res_data];
				invalidateAll();
			}
		} catch (error) {
			errors = ['Network error. Please try again.'];
		}
	};

	let showEditModal = $state(false);
	let edit_name = $state('');
	let edit_description = $state('');
	let edit_prep_time = $state(0);
	let edit_servings = $state(0);
	let edit_calories = $state(0);
	let edit_instructions = $state('');
	let edit_ingredients = $state('');

	const openEditModal = () => {
		edit_name = data.recipe.name;
		edit_description = data.recipe.description;
		edit_prep_time = data.recipe.prep_time;
		edit_servings = data.recipe.servings;
		edit_calories = data.recipe.calories;
		edit_instructions = data.recipe.instructions;
		edit_ingredients = JSON.stringify(ingredients, null, 2);
		showEditModal = true;
	};

	const handleRecipeEdit = async (event: Event) => {
		event.preventDefault();
		errors = [];

		try {
			const response = await fetch(`${env.PUBLIC_API_URL}/recipes/${recipe_id}`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify({
					name: edit_name,
					description: edit_description,
					prep_time: edit_prep_time,
					servings: edit_servings,
					calories: edit_calories,
					instructions: edit_instructions,
					ingredients: edit_ingredients,
					category_id: data.recipe.category_id
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
				showEditModal = false;
				invalidateAll();
			}
		} catch (error) {
			errors = ['Network error. Please try again.'];
		}
	};

	let showEditCommentModal = $state(false);
	let edit_comment_id = $state<number | null>(null);
	let edit_comment_title = $state('');
	let edit_comment_text = $state('');
	let edit_comment_rating = $state(5);

	// Function to open comment edit modal
	const openEditCommentModal = (comment: any) => {
		edit_comment_id = comment.id;
		edit_comment_title = comment.title;
		edit_comment_text = comment.text;
		edit_comment_rating = comment.rating;
		showEditCommentModal = true;
	};

	// Handle comment edit submission
	const handleCommentEdit = async (event: Event) => {
		event.preventDefault();
		errors = [];

		try {
			const response = await fetch(`${env.PUBLIC_API_URL}/comments/${edit_comment_id}`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify({
					title: edit_comment_title,
					text: edit_comment_text,
					rating: edit_comment_rating
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
				showEditCommentModal = false;
				invalidateAll();
			}
		} catch (error) {
			errors = ['Network error. Please try again.'];
		}
	};
</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
	<!-- Breadcrumb -->
	<div class="text-sm breadcrumbs mb-6">
		<ul>
			<li><a href="/" class="link link-hover">Home</a></li>
			<li><a href="/categories" class="link link-hover">Categories</a></li>
			<li>
				<a href="/categories/{data.recipe.category_id}/recipes" class="link link-hover"
					>{data.recipe.category_name}</a
				>
			</li>
			<li>{data.recipe.name}</li>
		</ul>
	</div>

	<div class="card bg-base-100 shadow-xl mb-6">
		<div class="card-body">
			<div class="badge badge-primary mb-3">{data.recipe.category_name}</div>
			<h1 class="card-title text-4xl mb-3">{data.recipe.name}</h1>
			{#if currentUser.logged_in && Number(currentUser.id) === Number(data.recipe.author_id)}
				<button class="btn btn-secondary btn-sm w-fit" onclick={openEditModal}>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="size-5"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
						/>
					</svg>
					Edit Recipe
				</button>
			{/if}
			<p class="text-base-content/70 text-lg">{data.recipe.description}</p>

			<div class="divider"></div>
			<div class="grid grid-cols-3 gap-4">
				<div class="stat p-4 bg-base-200 rounded-lg">
					<div class="stat-figure text-primary">
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
								d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
							/>
						</svg>
					</div>
					<div class="stat-title text-xs">Prep Time</div>
					<div class="stat-value text-2xl">{data.recipe.prep_time} min</div>
				</div>
				<div class="stat p-4 bg-base-200 rounded-lg">
					<div class="stat-figure text-secondary">
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
								d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
							/>
						</svg>
					</div>
					<div class="stat-title text-xs">Servings</div>
					<div class="stat-value text-2xl">{data.recipe.servings}</div>
				</div>
				<div class="stat p-4 bg-base-200 rounded-lg">
					<div class="stat-figure text-accent">
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
								d="M15.362 5.214A8.252 8.252 0 0 1 12 21 8.25 8.25 0 0 1 6.038 7.047 8.287 8.287 0 0 0 9 9.601a8.983 8.983 0 0 1 3.361-6.867 8.21 8.21 0 0 0 3 2.48Z"
							/>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M12 18a3.75 3.75 0 0 0 .495-7.468 5.99 5.99 0 0 0-1.925 3.547 5.975 5.975 0 0 1-2.133-1.001A3.75 3.75 0 0 0 12 18Z"
							/>
						</svg>
					</div>
					<div class="stat-title text-xs">Calories</div>
					<div class="stat-value text-2xl">{data.recipe.calories}</div>
				</div>
			</div>
		</div>
	</div>

	<div class="grid lg:grid-cols-3 gap-6">
		<div class="lg:col-span-1">
			<div class="card bg-base-100 shadow-xl">
				<div class="card-body">
					<h2 class="card-title text-2xl mb-4">Ingredients</h2>
					<ul class="space-y-3">
						{#each Object.entries(ingredients) as [ingredient, amount]}
							<li class="flex items-start">
								<input type="checkbox" class="checkbox checkbox-primary checkbox-sm mr-3 mt-1" />
								<div class="flex-1">
									<span class="font-medium capitalize">{ingredient}</span>
									<span class="text-base-content/60"> - {amount}</span>
								</div>
							</li>
						{/each}
					</ul>
				</div>
			</div>
		</div>

		<div class="lg:col-span-2">
			<div class="card bg-base-100 shadow-xl">
				<div class="card-body">
					<h2 class="card-title text-2xl mb-4">Instructions</h2>
					<div class="prose max-w-none">
						<p class="text-base leading-relaxed">{data.recipe.instructions}</p>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="card bg-base-100 shadow-xl mt-6">
		<div class="card-body">
			<h2 class="card-title text-2xl mb-4">Comments ({data.comments.length})</h2>

			{#if data.user}
				<!-- Comment Form -->
				<form class="mb-6">
					<div class="form-control mb-3">
						<label class="label" for="comment-title">
							<span class="label-text">Title</span>
						</label>
						<input
							bind:value={comment_title}
							type="text"
							id="comment-title"
							placeholder="Give your comment a title"
							class="input input-bordered w-full"
							required
						/>
					</div>

					<div class="form-control mb-3">
						<label class="label" for="comment-rating">
							<span class="label-text">Rating</span>
						</label>
						<select
							id="comment-rating"
							class="select select-bordered w-full"
							bind:value={comment_rating}
							required
						>
							<option value="5">5 - Excellent</option>
							<option value="4">4 - Very Good</option>
							<option value="3">3 - Good</option>
							<option value="2">2 - Fair</option>
							<option value="1">1 - Poor</option>
						</select>
					</div>

					<div class="form-control mb-4">
						<textarea
							id="comment-text"
							bind:value={comment_text}
							class="textarea textarea-bordered h-24 w-full"
							placeholder="Share your thoughts about this recipe..."
							required
						></textarea>
					</div>

					<button type="submit" class="btn btn-primary" onclick={handleComment}>Post Comment</button
					>
				</form>

				<div class="divider"></div>
			{/if}

			<!-- Comments List -->
			<div class="space-y-4">
				{#each data.comments as comment}
					<div class="card bg-base-200">
						<div class="card-body">
							<div class="flex justify-between items-start">
								<div class="flex-1">
									<div class="flex items-center gap-2 mb-2">
										<h3 class="font-bold text-lg">{comment.title}</h3>
										<div class="badge badge-warning gap-1">
											<svg
												xmlns="http://www.w3.org/2000/svg"
												fill="none"
												viewBox="0 0 24 24"
												stroke-width="1.5"
												stroke="currentColor"
												class="size-4"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z"
												/>
											</svg>
											{comment.rating}
										</div>
									</div>
									<p class="text-base-content/80">{comment.text}</p>
								</div>
								{#if currentUser.logged_in && (Number(currentUser.id) === Number(comment.user_id) || currentUser.role === 'ADMIN')}
									<div class="flex gap-1">
										{#if Number(currentUser.id) === Number(comment.user_id)}
											<button
												aria-label="edit"
												class="btn btn-ghost btn-sm text-blue-800"
												onclick={() => openEditCommentModal(comment)}
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
														d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
													/>
												</svg>
											</button>
										{/if}
										<button
											aria-label="delete"
											class="btn btn-ghost btn-sm text-error"
											onclick={(e) => handleCommentDelete(e, comment.id)}
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
													d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
												/>
											</svg>
										</button>
									</div>
								{/if}
							</div>
						</div>
					</div>
				{:else}
					<p class="text-center text-base-content/60 py-8">
						No comments yet. Be the first to share your thoughts!
					</p>
				{/each}
			</div>
		</div>
	</div>
	<!-- Edit Recipe Modal -->
	{#if showEditModal}
		<dialog class="modal modal-open">
			<div class="modal-box max-w-2xl">
				<h3 class="font-bold text-lg mb-4">Edit Recipe</h3>
				<form onsubmit={handleRecipeEdit}>
					<div class="form-control mb-3">
						<label class="label" for="edit-name">
							<span class="label-text">Recipe Name</span>
						</label>
						<input
							bind:value={edit_name}
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
							bind:value={edit_description}
							id="edit-description"
							class="textarea textarea-bordered h-20"
							required
						></textarea>
					</div>

					<div class="grid grid-cols-3 gap-3 mb-3">
						<div class="form-control">
							<label class="label" for="edit-prep-time">
								<span class="label-text">Prep Time (min)</span>
							</label>
							<input
								bind:value={edit_prep_time}
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
								bind:value={edit_servings}
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
								bind:value={edit_calories}
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
							bind:value={edit_ingredients}
							id="edit-ingredients"
							class="textarea textarea-bordered h-24 font-mono text-sm"
							required
						></textarea>
					</div>

					<div class="form-control mb-4">
						<label class="label" for="edit-instructions">
							<span class="label-text">Instructions</span>
						</label>
						<textarea
							bind:value={edit_instructions}
							id="edit-instructions"
							class="textarea textarea-bordered h-32"
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
						<button type="button" class="btn" onclick={() => (showEditModal = false)}>Cancel</button
						>
						<button type="submit" class="btn btn-primary">Save Changes</button>
					</div>
				</form>
			</div>
			<form method="dialog" class="modal-backdrop">
				<button onclick={() => (showEditModal = false)}>close</button>
			</form>
		</dialog>
	{/if}
	<!-- Edit Comment Modal -->
	{#if showEditCommentModal}
		<dialog class="modal modal-open">
			<div class="modal-box">
				<h3 class="font-bold text-lg mb-4">Edit Comment</h3>
				<form onsubmit={handleCommentEdit}>
					<div class="form-control mb-3">
						<label class="label" for="edit-comment-title">
							<span class="label-text">Title</span>
						</label>
						<input
							bind:value={edit_comment_title}
							type="text"
							id="edit-comment-title"
							placeholder="Give your comment a title"
							class="input input-bordered w-full"
							required
						/>
					</div>

					<div class="form-control mb-3">
						<label class="label" for="edit-comment-rating">
							<span class="label-text">Rating</span>
						</label>
						<select
							id="edit-comment-rating"
							class="select select-bordered w-full"
							bind:value={edit_comment_rating}
							required
						>
							<option value="5">5 - Excellent</option>
							<option value="4">4 - Very Good</option>
							<option value="3">3 - Good</option>
							<option value="2">2 - Fair</option>
							<option value="1">1 - Poor</option>
						</select>
					</div>

					<div class="form-control mb-4">
						<label class="label" for="edit-comment-text">
							<span class="label-text">Comment</span>
						</label>
						<textarea
							id="edit-comment-text"
							bind:value={edit_comment_text}
							class="textarea textarea-bordered h-24 w-full"
							placeholder="Share your thoughts about this recipe..."
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
						<button type="button" class="btn" onclick={() => (showEditCommentModal = false)}
							>Cancel</button
						>
						<button type="submit" class="btn btn-primary">Save Changes</button>
					</div>
				</form>
			</div>
			<form method="dialog" class="modal-backdrop">
				<button onclick={() => (showEditCommentModal = false)}>close</button>
			</form>
		</dialog>
	{/if}
</div>
