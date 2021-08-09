var registrationApp = angular.module('registrationModule', []);

registrationApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

registrationApp.controller(
	'registrationController',
	function($scope, $http) {
		$scope.editProfile = false;
		$scope.error = null;

		$scope.checkRegistration = function(event, email, newPassword, confirmPassword) {
			event.preventDefault();
			$scope.registerErrors = [];
			if(newPassword && confirmPassword) {
				if (newPassword != confirmPassword) {
					$scope.registerErrors = ['Passwords must match', ];
				} else {
					$scope.registerErrors = getPasswordErrors(newPassword);
				}
			}
			if (!$scope.registerErrors.length){
				$http.post(
						'/user/api/register/',
						{
							'request': 'check-id',
							'email': email
						}
					).then(function(response){
						if(response.data.status == 'ok') {
							$http.post(
								'/user/api/register/',
								{
									'request': 'register',
									'email': email,
									'password': newPassword
								}
							).then(function(response){
								window.location.href = '/user/login/?registered=true&id=' + email;
							});
						} else {
							$scope.registerErrors = response.data.errors;
						}
					});
			}
		}

		$scope.checkPassword = function(currentPassword, newPassword, confirmPassword) {
			$scope.passwordErrors = null;
			if(currentPassword && newPassword) {
				if (newPassword != confirmPassword) {
					$scope.passwordErrors = ['Passwords must match', ];
				} else {
					$scope.passwordErrors = getPasswordErrors(newPassword);
				}
				if (!$scope.passwordErrors.length){
					$http.post(
						'/user/api/register/',
						{
							'request': 'check-password',
							'password': currentPassword
						}
					).then(function(response){
						if(response.data.status == 'ok') {
							$http.post(
								'/api/profile/',
								{
									'request': 'set-password',
									'password': newPassword
								}
							).then(function(response){
								if(response.data.status == 'ok') {
									$scope.success = 'Password updated!';
									$scope.editPassword = false;
								} else {
									$scope.passwordErrors = [response.data.message, ];
								}
							});
						} else {
							$scope.passwordErrors = [response.data.message, ];
						}
					});
				}
			} 
		}
	}
);

angular.bootstrap(document.getElementById("registrationModule"), ['registrationModule']);
