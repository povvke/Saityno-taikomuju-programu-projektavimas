<script lang="ts">
	import './layout.css';
	import { currentUser } from '$lib/stores/state.svelte';
	import { onMount, onDestroy } from 'svelte';
	import favicon from '$lib/assets/favicon.svg';
	import { env } from '$env/dynamic/public';
	import { invalidateAll } from '$app/navigation';

	let { children, data } = $props();
	if (data.user) {
		currentUser.role = data.user.role ?? null;
		currentUser.id = data.user.id ?? null;
		currentUser.logged_in = data.user.id ? true : false;
	}
	let open = $state(false);
	let errors: string[] = $state([]);
	let email = $state('');
	let password = $state('');

	const handleSubmit = async (event: Event) => {
		event.preventDefault();
		errors = [];

		try {
			const response = await fetch(`${env.PUBLIC_API_URL}/auth/login`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify({ email, password })
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
				window.location.reload();
			}
		} catch (error) {
			errors = ['Network error. Please try again.'];
		}
	};

	const handleLogout = async (event: Event) => {
		event.preventDefault();
		await fetch(`${env.PUBLIC_API_URL}/auth/logout`, { method: 'POST', credentials: 'include' });
		currentUser.logged_in = false;
		invalidateAll();
	};

	function toggle(e: MouseEvent) {
		e.stopPropagation();
		open = !open;
	}

	function stop(e: Event) {
		e.stopPropagation();
	}

	function close() {
		open = false;
	}

	function onKey(e: KeyboardEvent) {
		if (e.key === 'Escape') close();
	}

	onMount(() => {
		if (typeof window === 'undefined') return;
		window.addEventListener('click', close);
		window.addEventListener('keydown', onKey);

		onDestroy(() => {
			window.removeEventListener('click', close);
			window.removeEventListener('keydown', onKey);
		});
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header class="navbar bg-base-200 px-4 shadow">
	<div class="flex-1">
		<a href="/" class="btn btn-ghost text-lg font-semibold">Home</a>
		<a href="/categories" class="btn btn-ghost">Categories</a>
	</div>

	<div class="flex-none">
		<div class="dropdown dropdown-end" class:dropdown-open={open}>
			{#if currentUser.logged_in}
				<span>{currentUser.role}</span>
			{:else}
				<span>Guest</span>
			{/if}
			<button
				aria-label="login"
				aria-haspopup="true"
				aria-expanded={open}
				class="btn btn-ghost btn-circle avatar"
				onclick={toggle}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="size-7"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z"
					/>
				</svg>
			</button>

			{#if currentUser.logged_in}
				<div
					class="menu dropdown-content mt-3 p-4 shadow bg-base-100 rounded-box w-72 space-y-3"
					role="menu"
					tabindex="0"
					onclick={stop}
					onkeydown={(e) => e.key === 'Escape' && close()}
				>
					<button onclick={handleLogout} class="btn btn-primary w-full">Logout</button>
				</div>
			{:else}
				<div
					class="menu dropdown-content mt-3 p-4 shadow bg-base-100 rounded-box w-72 space-y-3"
					role="menu"
					tabindex="0"
					onclick={stop}
					onkeydown={(e) => e.key === 'Escape' && close()}
				>
					<form class="flex flex-col space-y-2" onsubmit={close}>
						<input
							type="email"
							name="email"
							bind:value={email}
							placeholder="Email"
							class="input input-bordered w-full"
							required
						/>
						<input
							type="password"
							name="password"
							bind:value={password}
							placeholder="Password"
							class="input input-bordered w-full"
							required
						/>
						<button class="btn btn-primary w-full" onclick={handleSubmit}>Login</button>
					</form>

					<div class="divider my-0"></div>

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

					<a href="/register" class="btn btn-outline w-full">Register</a>
				</div>
			{/if}
		</div>
	</div>
</header>

{@render children?.()}

<footer class="footer items-center p-4 bg-base-200 text-base-content">
	<div class="container mx-auto flex justify-between">
		<span class="font-semibold text-lg">TasteHub</span>

		<a
			href="http://localhost:8000/docs"
			target="_blank"
			rel="noopener noreferrer"
			class="link link-hover"
		>
			API docs
		</a>
	</div>
</footer>
