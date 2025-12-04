<script lang="ts">
	let email = '';
	let username = '';
	let password = '';
	let loading = false;
	let errors: string[] = [];
	import { env } from '$env/dynamic/public';

	async function handleSubmit(event: Event) {
		event.preventDefault();
		loading = true;
		errors = [];

		try {
			const response = await fetch(`${env.PUBLIC_API_URL}/auth/register`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify({ email, username, password })
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
				window.location = '/';
			}
		} catch (error) {
			errors = ['Network error. Please try again.'];
		} finally {
			loading = false;
		}
	}
</script>

<div class="min-h-screen bg-base-200 flex items-center justify-center p-4">
	<div class="card w-full max-w-md bg-base-100 shadow-2xl">
		<div class="card-body">
			<h2 class="card-title text-3xl font-bold text-center justify-center mb-2">Create Account</h2>
			<p class="text-center text-base-content/60 mb-6">Join us today and get started</p>

			{#if errors.length > 0}
				<div class="alert alert-error mb-4">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="stroke-current shrink-0 h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
					<div class="flex flex-col gap-1">
						{#each errors as error}
							<span>{error}</span>
						{/each}
					</div>
				</div>
			{/if}

			<form on:submit={handleSubmit} class="space-y-4">
				<div class="form-control">
					<label class="label" for="email">
						<span class="label-text font-medium">Email</span>
					</label>
					<input
						id="email"
						type="email"
						bind:value={email}
						placeholder="your@email.com"
						class="input input-bordered w-full"
						required
					/>
				</div>

				<div class="form-control">
					<label class="label" for="username">
						<span class="label-text font-medium">Username</span>
					</label>
					<input
						id="username"
						type="text"
						bind:value={username}
						placeholder="Choose a username"
						class="input input-bordered w-full"
						required
					/>
				</div>

				<div class="form-control">
					<label class="label" for="password">
						<span class="label-text font-medium">Password</span>
					</label>
					<input
						id="password"
						type="password"
						bind:value={password}
						placeholder="••••••••"
						class="input input-bordered w-full"
						required
					/>
				</div>

				<div class="form-control mt-6">
					<button type="submit" class="btn btn-primary w-full" disabled={loading}>
						{#if loading}
							<span class="loading loading-spinner loading-sm"></span>
							Creating account...
						{:else}
							Register
						{/if}
					</button>
				</div>
			</form>

			<div class="divider">OR</div>

			<div class="text-center">
				<p class="text-sm text-base-content/60">
					Already have an account?
					<a href="/login" class="link link-primary font-medium"> Sign in </a>
				</p>
			</div>
		</div>
	</div>
</div>
